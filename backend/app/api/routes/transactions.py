from fastapi import APIRouter

from backend.app.db.database import SessionLocal
from backend.app.db.models import Transaction, Investigation


router = APIRouter(
    prefix="/api",
    tags=["Transactions"],
)


@router.get("/transactions")
def get_transactions():

    session = SessionLocal()

    try:
        transactions = (
            session.query(Transaction)
            .order_by(
                Transaction.timestamp.desc()
            )
            .all()
        )

        results = []

        for transaction in transactions:

            latest_investigation = (
                session.query(Investigation)
                .filter(
                    Investigation.transaction_id
                    == transaction.transaction_id
                )
                .order_by(
                    Investigation.created_at.desc()
                )
                .first()
            )

            results.append(
                {
                    "transaction_id": transaction.transaction_id,
                    "amount": transaction.amount,
                    "vendor_id": transaction.vendor_id,
                    "employee_id": transaction.employee_id,
                    "timestamp": transaction.timestamp,
                    "risk_level": (
                        latest_investigation.risk_level
                        if latest_investigation
                        else None
                    ),
                    "risk_score": (
                        latest_investigation.final_risk_score
                        if latest_investigation
                        else None
                    ),
                }
            )

        return results

    finally:
        session.close()