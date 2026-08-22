from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker


fake = Faker("en_US")

SEED = 42
random.seed(SEED)
Faker.seed(SEED)


def random_business_timestamp(
    unusual: bool = False,
) -> datetime:
    """Generate a normal or unusual transaction timestamp."""

    now = datetime.now()
    start = now - timedelta(days=365)

    timestamp = fake.date_time_between(
        start_date=start,
        end_date=now,
    )

    if unusual:
        hour = random.choice(
            [0, 1, 2, 3, 4, 22, 23]
        )
    else:
        hour = random.randint(9, 18)

    return timestamp.replace(
        hour=hour,
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
        microsecond=0,
    )


def generate_employees(count: int = 50) -> list[dict]:
    employees = []

    departments = [
        "Finance",
        "Procurement",
        "Operations",
        "Sales",
        "IT",
        "HR",
    ]

    role_limits = {
        "Analyst": 50_000,
        "Manager": 100_000,
        "Senior Manager": 250_000,
        "Director": 500_000,
        "VP": 1_000_000,
    }

    for index in range(1, count + 1):
        role = random.choice(list(role_limits.keys()))

        employees.append(
            {
                "employee_id": f"EMP-{index:04d}",
                "name": fake.name(),
                "department": random.choice(departments),
                "role": role,
                "authorization_limit": role_limits[role],
            }
        )

    return employees


def generate_bank_accounts(count: int = 120) -> list[dict]:
    bank_accounts = []

    banks = [
        "Chase Bank",
        "Bank of America",
        "Wells Fargo",
        "Citibank",
        "US Bank",
        "PNC Bank",
    ]

    for index in range(1, count + 1):
        bank_accounts.append(
            {
                "account_id": f"ACC-{index:05d}",
                "bank_name": random.choice(banks),
                "account_number_masked": (
                    f"****{random.randint(1000, 9999)}"
                ),
                "owner_entity": fake.company(),
                "created_at": fake.date_time_between(
                    start_date="-3y",
                    end_date="now",
                ),
            }
        )

    return bank_accounts


def generate_vendors(
    count: int = 100,
    bank_accounts: list[dict] | None = None,
) -> list[dict]:
    if not bank_accounts:
        raise ValueError(
            "bank_accounts are required to generate vendors"
        )

    vendors = []

    industries = [
        "Technology",
        "Construction",
        "Consulting",
        "Manufacturing",
        "Logistics",
        "Marketing",
        "Healthcare",
        "Professional Services",
    ]

    countries = [
        "United States",
        "Canada",
        "United Kingdom",
        "Germany",
        "India",
        "Singapore",
    ]

    for index in range(1, count + 1):
        bank_account = bank_accounts[
            (index - 1) % len(bank_accounts)
        ]

        vendors.append(
            {
                "vendor_id": f"VEN-{index:05d}",
                "company_name": fake.company(),
                "industry": random.choice(industries),
                "country": random.choice(countries),
                "bank_account_id": bank_account[
                    "account_id"
                ],
                "risk_history": "none",
            }
        )

    # Deliberate shared bank-account pattern.
    if count >= 3:
        shared_account = bank_accounts[0]["account_id"]

        vendors[0]["bank_account_id"] = shared_account
        vendors[1]["bank_account_id"] = shared_account
        vendors[2]["bank_account_id"] = shared_account

        vendors[1]["risk_history"] = "shared_account"
        vendors[2]["risk_history"] = "shared_account"

    return vendors


def generate_invoices(
    count: int = 500,
    vendors: list[dict] | None = None,
) -> list[dict]:
    if not vendors:
        raise ValueError(
            "vendors are required to generate invoices"
        )

    invoices = []

    statuses = [
        "pending",
        "approved",
        "paid",
        "rejected",
    ]

    for index in range(1, count + 1):
        vendor = random.choice(vendors)

        invoice_amount = round(
            random.uniform(5_000, 250_000),
            2,
        )

        invoices.append(
            {
                "invoice_id": f"INV-{index:06d}",
                "vendor_id": vendor["vendor_id"],
                "invoice_number": (
                    f"INVOICE-{index:06d}"
                ),
                "invoice_amount": invoice_amount,
                "invoice_date": fake.date_time_between(
                    start_date="-1y",
                    end_date="now",
                ),
                "status": random.choice(statuses),
            }
        )

    return invoices


def generate_transactions(
    count: int = 2_000,
    employees: list[dict] | None = None,
    vendors: list[dict] | None = None,
    bank_accounts: list[dict] | None = None,
    invoices: list[dict] | None = None,
) -> list[dict]:
    if not employees:
        raise ValueError(
            "employees are required to generate transactions"
        )

    if not vendors:
        raise ValueError(
            "vendors are required to generate transactions"
        )

    if not bank_accounts:
        raise ValueError(
            "bank_accounts are required to generate transactions"
        )

    if not invoices:
        raise ValueError(
            "invoices are required to generate transactions"
        )

    transactions = []

    payment_methods = [
        "ACH",
        "Wire",
        "Bank Transfer",
        "Check",
    ]

    locations = [
        "New York",
        "Chicago",
        "Los Angeles",
        "Houston",
        "Boston",
        "Seattle",
        "Dallas",
        "Atlanta",
    ]

    for index in range(1, count + 1):
        employee = random.choice(employees)
        vendor = random.choice(vendors)
        invoice = random.choice(invoices)

        pattern_roll = random.random()

        unusual_time = pattern_roll < 0.05
        high_amount = 0.05 <= pattern_roll < 0.10
        threshold_adjacent = (
            0.10 <= pattern_roll < 0.15
        )
        invoice_mismatch = (
            0.15 <= pattern_roll < 0.20
        )

        if high_amount:
            amount = round(
                random.uniform(500_000, 1_500_000),
                2,
            )

        elif threshold_adjacent:
            amount = round(
                employee["authorization_limit"]
                * random.uniform(0.95, 0.999),
                2,
            )

        elif invoice_mismatch:
            amount = round(
                invoice["invoice_amount"]
                * random.uniform(1.5, 3.0),
                2,
            )

        else:
            amount = round(
                random.uniform(5_000, 150_000),
                2,
            )

        bank_account_id = vendor["bank_account_id"]

        if random.random() < 0.03:
            bank_account_id = random.choice(
                bank_accounts
            )["account_id"]

        transactions.append(
            {
                "transaction_id": (
                    f"TX-{index:07d}"
                ),
                "timestamp": random_business_timestamp(
                    unusual=unusual_time,
                ),
                "amount": amount,
                "vendor_id": vendor["vendor_id"],
                "employee_id": employee[
                    "employee_id"
                ],
                "bank_account_id": bank_account_id,
                "location": random.choice(locations),
                "payment_method": random.choice(
                    payment_methods
                ),
                "invoice_id": invoice["invoice_id"],
                "approval_status": "pending",
            }
        )

    return transactions


def generate_approvals(
    transactions: list[dict] | None = None,
    employees: list[dict] | None = None,
) -> list[dict]:
    if not transactions:
        raise ValueError(
            "transactions are required to generate approvals"
        )

    if not employees:
        raise ValueError(
            "employees are required to generate approvals"
        )

    approvals = []

    employee_by_id = {
        employee["employee_id"]: employee
        for employee in employees
    }

    for index, transaction in enumerate(
        transactions,
        start=1,
    ):
        employee = employee_by_id[
            transaction["employee_id"]
        ]

        pattern_roll = random.random()

        if pattern_roll < 0.05:
            status = "missing"
            approved_at = None

        elif pattern_roll < 0.08:
            status = "rejected"

            approved_at = (
                transaction["timestamp"]
                + timedelta(
                    hours=random.randint(1, 24)
                )
            )

        else:
            status = "approved"

            approved_at = (
                transaction["timestamp"]
                + timedelta(
                    minutes=random.randint(5, 180)
                )
            )

        approvals.append(
            {
                "approval_id": f"APR-{index:07d}",
                "transaction_id": transaction[
                    "transaction_id"
                ],
                "employee_id": employee[
                    "employee_id"
                ],
                "approval_level": "standard",
                "status": status,
                "approved_at": approved_at,
            }
        )

    return approvals


def generate_incidents(
    count: int = 50,
    employees: list[dict] | None = None,
    vendors: list[dict] | None = None,
    bank_accounts: list[dict] | None = None,
) -> list[dict]:
    if not employees:
        raise ValueError(
            "employees are required to generate incidents"
        )

    if not vendors:
        raise ValueError(
            "vendors are required to generate incidents"
        )

    if not bank_accounts:
        raise ValueError(
            "bank_accounts are required to generate incidents"
        )

    incidents = []

    incident_types = [
        "suspicious_transaction",
        "policy_violation",
        "duplicate_payment",
        "unauthorized_payment",
        "vendor_risk",
        "account_anomaly",
    ]

    severities = [
        "low",
        "medium",
        "high",
        "critical",
    ]

    entities = []

    for employee in employees:
        entities.append(employee["employee_id"])

    for vendor in vendors:
        entities.append(vendor["vendor_id"])

    for account in bank_accounts:
        entities.append(account["account_id"])

    for index in range(1, count + 1):
        incident_type = random.choice(
            incident_types
        )

        severity = random.choice(severities)

        incident_date = fake.date_time_between(
            start_date="-2y",
            end_date="-30d",
        )

        entity_id = random.choice(entities)

        descriptions = {
            "suspicious_transaction": (
                "Transaction activity was flagged "
                "for unusual behavior."
            ),
            "policy_violation": (
                "Entity was associated with a "
                "potential policy violation."
            ),
            "duplicate_payment": (
                "Potential duplicate payment activity "
                "was identified."
            ),
            "unauthorized_payment": (
                "Payment activity appeared to lack "
                "appropriate authorization."
            ),
            "vendor_risk": (
                "Vendor was associated with "
                "historical risk indicators."
            ),
            "account_anomaly": (
                "Bank account activity showed "
                "unusual characteristics."
            ),
        }

        incidents.append(
            {
                "incident_id": f"INC-{index:05d}",
                "entity_id": entity_id,
                "incident_type": incident_type,
                "severity": severity,
                "date": incident_date,
                "description": descriptions[
                    incident_type
                ],
            }
        )

    return incidents


if __name__ == "__main__":
    employees = generate_employees()

    bank_accounts = generate_bank_accounts()

    vendors = generate_vendors(
        bank_accounts=bank_accounts,
    )

    invoices = generate_invoices(
        vendors=vendors,
    )

    transactions = generate_transactions(
        employees=employees,
        vendors=vendors,
        bank_accounts=bank_accounts,
        invoices=invoices,
    )

    approvals = generate_approvals(
        transactions=transactions,
        employees=employees,
    )

    incidents = generate_incidents(
        employees=employees,
        vendors=vendors,
        bank_accounts=bank_accounts,
    )

    print("\n--- EMPLOYEES ---")
    for employee in employees[:3]:
        print(employee)

    print("\n--- BANK ACCOUNTS ---")
    for account in bank_accounts[:3]:
        print(account)

    print("\n--- VENDORS ---")
    for vendor in vendors[:5]:
        print(vendor)

    print("\n--- INVOICES ---")
    for invoice in invoices[:3]:
        print(invoice)

    print("\n--- TRANSACTIONS ---")
    for transaction in transactions[:5]:
        print(transaction)

    print("\n--- APPROVALS ---")
    for approval in approvals[:5]:
        print(approval)

    print("\n--- INCIDENTS ---")
    for incident in incidents[:5]:
        print(incident)

    print("\n--- COUNTS ---")
    print(f"Employees: {len(employees)}")
    print(f"Bank Accounts: {len(bank_accounts)}")
    print(f"Vendors: {len(vendors)}")
    print(f"Invoices: {len(invoices)}")
    print(f"Transactions: {len(transactions)}")
    print(f"Approvals: {len(approvals)}")
    print(f"Incidents: {len(incidents)}")