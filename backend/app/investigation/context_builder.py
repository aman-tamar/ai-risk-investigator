from __future__ import annotations

from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.db.models import (
    Approval,
    BankAccount,
    Employee,
    Incident,
    Invoice,
    Transaction,
    Vendor,
)


def build_investigation_context(
    transaction_id: str,
) -> dict:
    session = SessionLocal()

    try:
        transaction = session.get(
            Transaction,
            transaction_id,
        )

        if transaction is None:
            raise ValueError(
                f"Transaction not found: {transaction_id}"
            )

        employee = session.get(
            Employee,
            transaction.employee_id,
        )

        vendor = session.get(
            Vendor,
            transaction.vendor_id,
        )

        bank_account = session.get(
            BankAccount,
            transaction.bank_account_id,
        )

        invoice = session.get(
            Invoice,
            transaction.invoice_id,
        )

        approvals = session.scalars(
            select(Approval).where(
                Approval.transaction_id
                == transaction.transaction_id
            )
        ).all()

        employee_incidents = session.scalars(
            select(Incident).where(
                Incident.entity_id
                == transaction.employee_id
            )
        ).all()

        vendor_incidents = session.scalars(
            select(Incident).where(
                Incident.entity_id
                == transaction.vendor_id
            )
        ).all()

        account_incidents = session.scalars(
            select(Incident).where(
                Incident.entity_id
                == transaction.bank_account_id
            )
        ).all()

        related_vendors = session.scalars(
            select(Vendor).where(
                Vendor.bank_account_id
                == transaction.bank_account_id
            )
        ).all()

        context = {
            "transaction": {
                "transaction_id": transaction.transaction_id,
                "timestamp": transaction.timestamp,
                "amount": float(transaction.amount),
                "vendor_id": transaction.vendor_id,
                "employee_id": transaction.employee_id,
                "bank_account_id": transaction.bank_account_id,
                "location": transaction.location,
                "payment_method": transaction.payment_method,
                "invoice_id": transaction.invoice_id,
                "approval_status": transaction.approval_status,
            },
            "employee": None,
            "vendor": None,
            "bank_account": None,
            "invoice": None,
            "approvals": [],
            "historical_incidents": [],
            "related_vendors": [],
        }

        if employee:
            context["employee"] = {
                "employee_id": employee.employee_id,
                "name": employee.name,
                "department": employee.department,
                "role": employee.role,
                "authorization_limit": float(
                    employee.authorization_limit
                ),
            }

        if vendor:
            context["vendor"] = {
                "vendor_id": vendor.vendor_id,
                "company_name": vendor.company_name,
                "industry": vendor.industry,
                "country": vendor.country,
                "bank_account_id": vendor.bank_account_id,
                "risk_history": vendor.risk_history,
            }

        if bank_account:
            context["bank_account"] = {
                "account_id": bank_account.account_id,
                "bank_name": bank_account.bank_name,
                "account_number_masked": (
                    bank_account.account_number_masked
                ),
                "owner_entity": bank_account.owner_entity,
                "created_at": bank_account.created_at,
            }

        if invoice:
            context["invoice"] = {
                "invoice_id": invoice.invoice_id,
                "vendor_id": invoice.vendor_id,
                "invoice_number": invoice.invoice_number,
                "invoice_amount": float(
                    invoice.invoice_amount
                ),
                "invoice_date": invoice.invoice_date,
                "status": invoice.status,
            }

        context["approvals"] = [
            {
                "approval_id": approval.approval_id,
                "employee_id": approval.employee_id,
                "approval_level": approval.approval_level,
                "status": approval.status,
                "approved_at": approval.approved_at,
            }
            for approval in approvals
        ]

        context["historical_incidents"] = [
            {
                "incident_id": incident.incident_id,
                "entity_id": incident.entity_id,
                "incident_type": incident.incident_type,
                "severity": incident.severity,
                "date": incident.date,
                "description": incident.description,
            }
            for incident in (
                employee_incidents
                + vendor_incidents
                + account_incidents
            )
        ]

        context["related_vendors"] = [
            {
                "vendor_id": related_vendor.vendor_id,
                "company_name": related_vendor.company_name,
                "bank_account_id": (
                    related_vendor.bank_account_id
                ),
                "risk_history": (
                    related_vendor.risk_history
                ),
            }
            for related_vendor in related_vendors
        ]

        return context

    finally:
        session.close()


if __name__ == "__main__":
    transaction_id = "TX-0000001"

    context = build_investigation_context(
        transaction_id
    )

    print("\n--- INVESTIGATION CONTEXT ---")

    for section, data in context.items():
        print(f"\n[{section}]")
        print(data)