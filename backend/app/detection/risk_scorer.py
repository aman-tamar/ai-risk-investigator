from __future__ import annotations

import pandas as pd

from backend.app.detection.anomaly_detector import (
    TransactionAnomalyDetector,
)
from backend.app.detection.features import (
    build_features,
    get_model_features,
    load_transaction_data,
)
from backend.app.detection.risk_rules import (
    run_rule_detection,
)


def calculate_ml_score(
    anomaly_scores: pd.Series,
) -> pd.Series:
    """
    Convert Isolation Forest decision scores into
    a normalized 0-100 anomaly score.

    Lower Isolation Forest scores indicate stronger
    anomalies, so the value is inverted.
    """

    minimum = anomaly_scores.min()
    maximum = anomaly_scores.max()

    if maximum == minimum:
        return pd.Series(
            0.0,
            index=anomaly_scores.index,
        )

    normalized = (
        (maximum - anomaly_scores)
        / (maximum - minimum)
    )

    return normalized * 100


def calculate_final_risk_score(
    results: pd.DataFrame,
) -> pd.DataFrame:
    df = results.copy()

    # ML contributes 40% of the final score.
    df["ml_score"] = calculate_ml_score(
        df["anomaly_score"]
    )

    # Rules contribute 60%.
    df["final_risk_score"] = (
        df["ml_score"] * 0.40
        + df["rule_score"] * 0.60
    )

    df["final_risk_score"] = (
        df["final_risk_score"]
        .clip(0, 100)
        .round(2)
    )

    df["risk_level"] = pd.cut(
        df["final_risk_score"],
        bins=[
            -0.01,
            25,
            50,
            75,
            100,
        ],
        labels=[
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        ],
    )

    return df


def build_risk_scores() -> pd.DataFrame:
    transactions = load_transaction_data()

    features = build_features(
        transactions
    )

    # -----------------------------
    # ML anomaly detection
    # -----------------------------

    detector = TransactionAnomalyDetector()

    detector.fit(features)

    ml_results = detector.predict(
        features
    )

    # -----------------------------
    # Rule-based detection
    # -----------------------------

    rule_results = run_rule_detection(
        features
    )

    # Keep the rule signals and score.
    rule_columns = [
        "transaction_id",
        "authorization_violation",
        "invoice_mismatch",
        "after_hours_risk",
        "shared_account_risk",
        "historical_vendor_risk",
        "threshold_risk",
        "rule_score",
    ]

    rule_results = rule_results[
        rule_columns
    ]

    # -----------------------------
    # Combine ML + rules
    # -----------------------------

    results = ml_results.merge(
        rule_results,
        on="transaction_id",
        how="left",
    )

    return calculate_final_risk_score(
        results
    )


if __name__ == "__main__":
    results = build_risk_scores()

    columns = [
        "transaction_id",
        "amount",
        "anomaly_score",
        "ml_score",
        "rule_score",
        "final_risk_score",
        "risk_level",
    ]

    print("\n--- FINAL RISK SCORES ---")

    print(
        results[
            columns
        ]
        .sort_values(
            "final_risk_score",
            ascending=False,
        )
        .head(20)
        .to_string(index=False)
    )

    print("\n--- RISK LEVEL SUMMARY ---")

    print(
        results["risk_level"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\n--- SCORE SUMMARY ---")

    print(
        f"Transactions analyzed: "
        f"{len(results)}"
    )

    print(
        f"Average risk score: "
        f"{results['final_risk_score'].mean():.2f}"
    )

    print(
        f"Maximum risk score: "
        f"{results['final_risk_score'].max():.2f}"
    )