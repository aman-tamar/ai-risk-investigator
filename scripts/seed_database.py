from __future__ import annotations

from sqlalchemy import delete

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
from scripts.generate_data import (
    generate_approvals,
    generate_bank_accounts,
    generate_employees,
    generate_incidents,
    generate_invoices,
    generate_transactions,
    generate_vendors,
)


def clear_database(session) -> None:
    """Delete existing data in foreign-key dependency order."""

    session.execute(delete(Approval))
    session.execute(delete(Transaction))
    session.execute(delete(Invoice))
    session.execute(delete(Incident))
    session.execute(delete(Vendor))
    session.execute(delete(BankAccount))
    session.execute(delete(Employee))


def seed_database() -> None:
    session = SessionLocal()

    try:
        print("Clearing existing data...")
        clear_database(session)

        print("Generating employees...")
        employees_data = generate_employees(50)

        print("Generating bank accounts...")
        bank_accounts_data = generate_bank_accounts(120)

        print("Generating vendors...")
        vendors_data = generate_vendors(
            100,
            bank_accounts_data,
        )

        print("Generating invoices...")
        invoices_data = generate_invoices(
            500,
            vendors_data,
        )

        print("Generating transactions...")
        transactions_data = generate_transactions(
            2_000,
            employees_data,
            vendors_data,
            bank_accounts_data,
            invoices_data,
        )

        print("Generating approvals...")
        approvals_data = generate_approvals(
            transactions_data,
            employees_data,
        )

        print("Generating incidents...")
        incidents_data = generate_incidents(
            50,
            employees_data,
            vendors_data,
            bank_accounts_data,
        )

        print("Creating database objects...")

        employees = [
            Employee(**employee)
            for employee in employees_data
        ]

        bank_accounts = [
            BankAccount(**account)
            for account in bank_accounts_data
        ]

        vendors = [
            Vendor(**vendor)
            for vendor in vendors_data
        ]

        invoices = [
            Invoice(**invoice)
            for invoice in invoices_data
        ]

        transactions = [
            Transaction(**transaction)
            for transaction in transactions_data
        ]

        approvals = [
            Approval(**approval)
            for approval in approvals_data
        ]

        incidents = [
            Incident(**incident)
            for incident in incidents_data
        ]

        print("Inserting employees...")
        session.add_all(employees)
        session.flush()

        print("Inserting bank accounts...")
        session.add_all(bank_accounts)
        session.flush()

        print("Inserting vendors...")
        session.add_all(vendors)
        session.flush()

        print("Inserting invoices...")
        session.add_all(invoices)
        session.flush()

        print("Inserting transactions...")
        session.add_all(transactions)
        session.flush()

        print("Inserting approvals...")
        session.add_all(approvals)
        session.flush()

        print("Inserting incidents...")
        session.add_all(incidents)
        session.flush()

        session.commit()

        print("\nDatabase seeded successfully!")
        print(f"Employees: {len(employees)}")
        print(f"Bank Accounts: {len(bank_accounts)}")
        print(f"Vendors: {len(vendors)}")
        print(f"Invoices: {len(invoices)}")
        print(f"Transactions: {len(transactions)}")
        print(f"Approvals: {len(approvals)}")
        print(f"Incidents: {len(incidents)}")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    seed_database()