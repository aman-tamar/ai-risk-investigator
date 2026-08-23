from __future__ import annotations

import pandas as pd

from backend.app.db.database import SessionLocal
from backend.app.db.models import (
    Approval,
    Incident,
    Invoice,
)


def add_relational_signals(
    features: pd.DataFrame,
) -> pd.DataFrame:

    df = features.copy()

    # ---------------------------------------
    # Existing rule signals
    # ---------------------------------------

    df["authorization_violation"] = (
        df["amount"]
        >
        df["authorization_limit"]
    ).astype(int)


    df["invoice_mismatch"] = (
        df["amount_to_invoice_ratio"]
        >= 1.5
    ).astype(int)


    df["after_hours_risk"] = (
        df["is_after_hours"]
        == 1
    ).astype(int)


    df["shared_account_risk"] = (
        df["shared_bank_account"]
        == 1
    ).astype(int)


    df["historical_vendor_risk"] = (
        df["has_vendor_risk_history"]
        == 1
    ).astype(int)


    df["threshold_risk"] = (
        df["amount_to_authorization_ratio"]
        >= 0.95
    ).astype(int)


    # ---------------------------------------
    # New relational signals
    # ---------------------------------------

    session = SessionLocal()

    try:

        invoices = {
            invoice.invoice_id: invoice.vendor_id
            for invoice in session.query(
                Invoice
            ).all()
        }

        df["invoice_vendor_mismatch"] = (
            df.apply(
                lambda row:
                1
                if invoices.get(
                    row["invoice_id"]
                )
                != row["vendor_id"]
                else 0,
                axis=1,
            )
        )


        approvals = session.query(
            Approval
        ).all()

        approval_map = {}

        for approval in approvals:
            approval_map[
                approval.transaction_id
            ] = approval.employee_id


        df["self_approval"] = (
            df.apply(
                lambda row:
                1
                if approval_map.get(
                    row["transaction_id"]
                )
                ==
                row["employee_id"]
                else 0,
                axis=1,
            )
        )


        incidents = session.query(
            Incident
        ).all()


        risky_entities = {
            incident.entity_id
            for incident in incidents
            if incident.severity
            in [
                "high",
                "critical",
            ]
        }


        df["historical_incident"] = (
            df.apply(
                lambda row:
                1
                if (
                    row["vendor_id"]
                    in risky_entities
                    or
                    row["bank_account_id"]
                    in risky_entities
                    or
                    row["employee_id"]
                    in risky_entities
                )
                else 0,
                axis=1,
            )
        )


        return df

    finally:
        session.close()



def calculate_rule_score(
    features: pd.DataFrame,
) -> pd.DataFrame:

    df = features.copy()


    df["rule_score"] = (

        # Existing rules
        df["authorization_violation"] * 25

        + df["invoice_mismatch"] * 15

        + df["after_hours_risk"] * 10

        + df["shared_account_risk"] * 15

        + df["historical_vendor_risk"] * 10

        + df["threshold_risk"] * 5


        # New relational rules
        + df["invoice_vendor_mismatch"] * 15

        + df["self_approval"] * 10

        + df["historical_incident"] * 15

    )


    return df



def run_rule_detection(
    features: pd.DataFrame,
) -> pd.DataFrame:

    df = add_relational_signals(
        features
    )

    df = calculate_rule_score(
        df
    )

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


    print(
        results[
            [
                "transaction_id",
                "rule_score",
                "invoice_vendor_mismatch",
                "self_approval",
                "historical_incident",
            ]
        ]
        .sort_values(
            "rule_score",
            ascending=False,
        )
        .head(20)
        .to_string(index=False)
    )