from __future__ import annotations

import pandas as pd
from sqlalchemy import text

from backend.app.db.database import engine


def load_transaction_data() -> pd.DataFrame:
    query = text(
        """
        SELECT
            t.transaction_id,
            t.timestamp,
            t.amount,
            t.vendor_id,
            t.employee_id,
            t.bank_account_id,
            t.location,
            t.payment_method,
            t.invoice_id,
            t.approval_status,

            e.authorization_limit,

            i.invoice_amount,

            v.risk_history

        FROM transactions t

        JOIN employees e
            ON t.employee_id = e.employee_id

        JOIN invoices i
            ON t.invoice_id = i.invoice_id

        JOIN vendors v
            ON t.vendor_id = v.vendor_id
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


def build_features(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    df = transactions.copy()

    # ---------------------------------------------------------
    # Time-based features
    # ---------------------------------------------------------

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["transaction_hour"] = (
        df["timestamp"].dt.hour
    )

    df["day_of_week"] = (
        df["timestamp"].dt.dayofweek
    )

    df["is_weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    df["is_after_hours"] = (
        (df["transaction_hour"] < 9)
        | (df["transaction_hour"] > 18)
    ).astype(int)

    # ---------------------------------------------------------
    # Amount-based features
    # ---------------------------------------------------------

    df["amount_to_authorization_ratio"] = (
        df["amount"]
        / df["authorization_limit"]
    )

    df["amount_to_invoice_ratio"] = (
        df["amount"]
        / df["invoice_amount"].replace(0, 1)
    )

    df["invoice_amount_difference"] = (
        df["amount"]
        - df["invoice_amount"]
    )

    df["amount_above_authorization"] = (
        df["amount"]
        > df["authorization_limit"]
    ).astype(int)

    # ---------------------------------------------------------
    # Transaction frequency features
    # ---------------------------------------------------------

    df["vendor_transaction_count"] = (
        df.groupby("vendor_id")[
            "transaction_id"
        ].transform("count")
    )

    df["employee_transaction_count"] = (
        df.groupby("employee_id")[
            "transaction_id"
        ].transform("count")
    )

    df["bank_account_transaction_count"] = (
        df.groupby("bank_account_id")[
            "transaction_id"
        ].transform("count")
    )

    # ---------------------------------------------------------
    # Shared account feature
    # ---------------------------------------------------------

    df["vendors_per_bank_account"] = (
        df.groupby("bank_account_id")[
            "vendor_id"
        ].transform("nunique")
    )

    df["shared_bank_account"] = (
        df["vendors_per_bank_account"] > 1
    ).astype(int)

    # ---------------------------------------------------------
    # Historical vendor risk
    # ---------------------------------------------------------

    df["has_vendor_risk_history"] = (
        df["risk_history"] != "none"
    ).astype(int)

    return df


def get_model_features(
    features: pd.DataFrame,
) -> pd.DataFrame:
    model_columns = [
        "amount",
        "transaction_hour",
        "day_of_week",
        "is_weekend",
        "is_after_hours",
        "amount_to_authorization_ratio",
        "amount_to_invoice_ratio",
        "invoice_amount_difference",
        "amount_above_authorization",
        "vendor_transaction_count",
        "employee_transaction_count",
        "bank_account_transaction_count",
        "vendors_per_bank_account",
        "shared_bank_account",
        "has_vendor_risk_history",
    ]

    return features[model_columns].copy()


if __name__ == "__main__":
    transactions = load_transaction_data()

    features = build_features(transactions)

    model_features = get_model_features(
        features
    )

    print("\n--- RAW TRANSACTION DATA ---")
    print(transactions.head())

    print("\n--- ENGINEERED FEATURES ---")
    print(model_features.head())

    print("\n--- FEATURE SHAPE ---")
    print(model_features.shape)