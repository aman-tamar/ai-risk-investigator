from __future__ import annotations

import pandas as pd


def calculate_rule_signals(
    features: pd.DataFrame,
) -> pd.DataFrame:
    df = features.copy()

    # Amount exceeds employee authorization limit
    df["authorization_violation"] = (
        df["amount"] > df["authorization_limit"]
    ).astype(int)

    # Transaction amount significantly differs from invoice
    df["invoice_mismatch"] = (
        df["amount_to_invoice_ratio"] >= 1.5
    ).astype(int)

    # Transaction happened outside normal business hours
    df["after_hours_risk"] = (
        df["is_after_hours"] == 1
    ).astype(int)

    # Multiple vendors use the same bank account
    df["shared_account_risk"] = (
        df["shared_bank_account"] == 1
    ).astype(int)

    # Vendor already has historical risk
    df["historical_vendor_risk"] = (
        df["has_vendor_risk_history"] == 1
    ).astype(int)

    # Transaction is very close to authorization limit
    df["threshold_risk"] = (
        df["amount_to_authorization_ratio"] >= 0.95
    ).astype(int)

    return df


def calculate_rule_score(
    features: pd.DataFrame,
) -> pd.DataFrame:
    df = features.copy()

    df["rule_score"] = (
        df["authorization_violation"] * 30
        + df["invoice_mismatch"] * 20
        + df["after_hours_risk"] * 15
        + df["shared_account_risk"] * 15
        + df["historical_vendor_risk"] * 10
        + df["threshold_risk"] * 10
    )

    return df


def run_rule_detection(
    features: pd.DataFrame,
) -> pd.DataFrame:
    df = calculate_rule_signals(features)

    df = calculate_rule_score(df)

    return df


if __name__ == "__main__":
    from backend.app.detection.features import (
        build_features,
        load_transaction_data,
    )

    transactions = load_transaction_data()

    features = build_features(
        transactions
    )

    results = run_rule_detection(
        features
    )

    signal_columns = [
        "transaction_id",
        "amount",
        "authorization_violation",
        "invoice_mismatch",
        "after_hours_risk",
        "shared_account_risk",
        "historical_vendor_risk",
        "threshold_risk",
        "rule_score",
    ]

    print("\n--- RULE-BASED RISK SIGNALS ---")

    print(
        results[
            signal_columns
        ]
        .sort_values(
            "rule_score",
            ascending=False,
        )
        .head(20)
        .to_string(index=False)
    )

    print("\n--- RULE SCORE SUMMARY ---")

    print(
        f"Transactions analyzed: {len(results)}"
    )

    print(
        f"Transactions with rule score > 0: "
        f"{(results['rule_score'] > 0).sum()}"
    )

    print(
        f"Maximum rule score: "
        f"{results['rule_score'].max()}"
    )