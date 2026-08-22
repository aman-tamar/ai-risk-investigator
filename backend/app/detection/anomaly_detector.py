from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest

from backend.app.detection.features import (
    build_features,
    get_model_features,
    load_transaction_data,
)


class TransactionAnomalyDetector:
    def __init__(
        self,
        contamination: float = 0.05,
        random_state: int = 42,
    ) -> None:
        self.model = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1,
        )

    def fit(
        self,
        features: pd.DataFrame,
    ) -> None:
        model_features = get_model_features(
            features
        )

        self.model.fit(model_features)

    def predict(
        self,
        features: pd.DataFrame,
    ) -> pd.DataFrame:
        model_features = get_model_features(
            features
        )

        predictions = self.model.predict(
            model_features
        )

        anomaly_scores = self.model.decision_function(
            model_features
        )

        results = features[
            [
                "transaction_id",
                "timestamp",
                "amount",
                "vendor_id",
                "employee_id",
                "bank_account_id",
                "invoice_id",
            ]
        ].copy()

        results["anomaly_prediction"] = predictions

        results["anomaly_score"] = anomaly_scores

        results["is_anomaly"] = (
            predictions == -1
        )

        return results


def run_anomaly_detection() -> pd.DataFrame:
    transactions = load_transaction_data()

    features = build_features(
        transactions
    )

    detector = TransactionAnomalyDetector()

    detector.fit(features)

    results = detector.predict(
        features
    )

    return results


if __name__ == "__main__":
    results = run_anomaly_detection()

    print("\n--- ANOMALY DETECTION RESULTS ---")

    print(
        results[
            [
                "transaction_id",
                "amount",
                "anomaly_score",
                "is_anomaly",
            ]
        ]
        .sort_values("anomaly_score")
        .head(20)
        .to_string(index=False)
    )

    print("\n--- SUMMARY ---")

    print(
        f"Total transactions: {len(results)}"
    )

    print(
        f"Anomalies detected: "
        f"{results['is_anomaly'].sum()}"
    )

    print(
        f"Anomaly percentage: "
        f"{results['is_anomaly'].mean() * 100:.2f}%"
    )