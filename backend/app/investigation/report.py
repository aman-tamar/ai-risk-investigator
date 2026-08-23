from __future__ import annotations

from backend.app.investigation.evidence import (
    build_evidence_package,
)


def build_investigation_report(
    transaction_id: str,
) -> dict:
    evidence = build_evidence_package(
        transaction_id
    )

    transaction = evidence["context"]["transaction"]
    employee = evidence["context"]["employee"]
    vendor = evidence["context"]["vendor"]
    invoice = evidence["context"]["invoice"]

    risk = evidence["risk_assessment"]
    signals = evidence["risk_signals"]

    report = {
        "transaction_id": transaction_id,
        "risk_level": risk["risk_level"],
        "risk_score": risk["final_risk_score"],
        "summary": (
            f"Transaction {transaction_id} has a "
            f"{risk['risk_level']} risk level with "
            f"a risk score of "
            f"{risk['final_risk_score']:.2f}."
        ),
        "transaction": {
            "amount": transaction["amount"],
            "timestamp": transaction["timestamp"],
            "payment_method": transaction[
                "payment_method"
            ],
            "location": transaction["location"],
        },
        "employee": employee,
        "vendor": vendor,
        "invoice": invoice,
        "risk_signals": signals,
        "related_vendors": evidence[
            "context"
        ]["related_vendors"],
        "historical_incidents": evidence[
            "context"
        ]["historical_incidents"],
        "approvals": evidence[
            "context"
        ]["approvals"],
        "ml_score": risk["ml_score"],
        "rule_score": risk["rule_score"],
    }

    return report


def print_report(report: dict) -> None:
    print("\n" + "=" * 60)
    print("AI RISK INVESTIGATION REPORT")
    print("=" * 60)

    print(
        f"\nTransaction ID : "
        f"{report['transaction_id']}"
    )

    print(
        f"Risk Level     : "
        f"{report['risk_level']}"
    )

    print(
        f"Risk Score     : "
        f"{report['risk_score']}"
    )

    print(
        f"ML Score       : "
        f"{report['ml_score']:.2f}"
    )

    print(
        f"Rule Score     : "
        f"{report['rule_score']:.2f}"
    )

    print("\n--- SUMMARY ---")
    print(report["summary"])

    print("\n--- TRANSACTION ---")

    transaction = report["transaction"]

    print(
        f"Amount         : "
        f"{transaction['amount']}"
    )

    print(
        f"Timestamp      : "
        f"{transaction['timestamp']}"
    )

    print(
        f"Payment Method : "
        f"{transaction['payment_method']}"
    )

    print(
        f"Location       : "
        f"{transaction['location']}"
    )

    print("\n--- EMPLOYEE ---")

    print(report["employee"])

    print("\n--- VENDOR ---")

    print(report["vendor"])

    print("\n--- INVOICE ---")

    print(report["invoice"])

    print("\n--- RISK SIGNALS ---")

    for signal in report["risk_signals"]:
        print(f"- {signal}")

    print("\n--- RELATED VENDORS ---")

    for vendor in report["related_vendors"]:
        print(vendor)

    print("\n--- HISTORICAL INCIDENTS ---")

    for incident in report[
        "historical_incidents"
    ]:
        print(incident)

    print("\n--- APPROVALS ---")

    for approval in report["approvals"]:
        print(approval)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    transaction_id = "TX-0000001"

    report = build_investigation_report(
        transaction_id
    )

    print_report(report)