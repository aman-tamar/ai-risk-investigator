from __future__ import annotations

import pandas as pd

from backend.app.detection.risk_scorer import (
    build_risk_scores,
)
from backend.app.investigation.context_builder import (
    build_investigation_context,
)


def build_evidence_package(
    transaction_id: str,
) -> dict:
    """
    Build a complete evidence package for a transaction.

    Combines:
    - Transaction context
    - ML anomaly score
    - Rule-based signals
    - Final risk score
    - Related entities
    """

    risk_results = build_risk_scores()

    transaction_results = risk_results[
        risk_results["transaction_id"]
        == transaction_id
    ]

    if transaction_results.empty:
        raise ValueError(
            f"Transaction not found in risk results: "
            f"{transaction_id}"
        )

    risk_row = transaction_results.iloc[0]

    context = build_investigation_context(
        transaction_id
    )

    signals = []

    if risk_row["authorization_violation"] == 1:
        signals.append(
            "Transaction exceeds the employee authorization limit."
        )

    if risk_row["invoice_mismatch"] == 1:
        signals.append(
            "Transaction amount significantly differs from the invoice amount."
        )

    if risk_row["after_hours_risk"] == 1:
        signals.append(
            "Transaction occurred outside normal business hours."
        )

    if risk_row["shared_account_risk"] == 1:
        signals.append(
            "Multiple vendors are associated with the same bank account."
        )

    if risk_row["historical_vendor_risk"] == 1:
        signals.append(
            "The vendor has historical risk indicators."
        )

    if risk_row["threshold_risk"] == 1:
        signals.append(
            "Transaction amount is close to the employee authorization threshold."
        )

    if risk_row["invoice_vendor_mismatch"] == 1:
        signals.append(
            "Invoice vendor does not match the transaction vendor."
        )

    if risk_row["self_approval"] == 1:
        signals.append(
            "Transaction was approved by the same employee who initiated it."
        )

    if risk_row["historical_incident"] == 1:
        signals.append(
            "Related entity has previous high-severity incidents."
        )

    if not signals:
        signals.append(
            "No deterministic risk rule was triggered."
        )

    evidence = {
        "transaction_id": transaction_id,
        "risk_assessment": {
            "ml_score": round(
                float(risk_row["ml_score"]),
                2,
            ),
            "rule_score": round(
                float(risk_row["rule_score"]),
                2,
            ),
            "final_risk_score": round(
                float(risk_row["final_risk_score"]),
                2,
            ),
            "risk_level": str(
                risk_row["risk_level"]
            ),
        },
        "risk_signals": signals,
        "context": context,
    }

    return evidence


if __name__ == "__main__":
    transaction_id = "TX-0000001"

    evidence = build_evidence_package(
        transaction_id
    )

    print("\n--- RISK ASSESSMENT ---")

    print(
        evidence["risk_assessment"]
    )

    print("\n--- RISK SIGNALS ---")

    for signal in evidence["risk_signals"]:
        print(f"- {signal}")

    print("\n--- RELATED VENDORS ---")

    for vendor in evidence["context"][
        "related_vendors"
    ]:
        print(vendor)

    print("\n--- INVESTIGATION CONTEXT ---")

    for section, data in evidence[
        "context"
    ].items():
        print(f"\n[{section}]")
        print(data)