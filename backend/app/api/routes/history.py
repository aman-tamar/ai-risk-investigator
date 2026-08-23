from fastapi import APIRouter, HTTPException

from backend.app.db.database import SessionLocal
from backend.app.db.models import Investigation


router = APIRouter(
    prefix="/api",
    tags=["Investigation History"],
)


@router.get("/investigations")
def get_investigations():

    session = SessionLocal()

    try:
        investigations = (
            session.query(Investigation)
            .order_by(
                Investigation.created_at.desc()
            )
            .all()
        )

        return [
            {
                "id": item.id,
                "transaction_id": item.transaction_id,
                "risk_level": item.risk_level,
                "final_risk_score": item.final_risk_score,
                "confidence": item.confidence,
                "created_at": item.created_at,
            }
            for item in investigations
        ]

    finally:
        session.close()



@router.get(
    "/investigations/{transaction_id}"
)
def get_investigation(
    transaction_id: str,
):

    session = SessionLocal()

    try:
        investigation = (
            session.query(Investigation)
            .filter(
                Investigation.transaction_id
                == transaction_id
            )
            .order_by(
                Investigation.created_at.desc()
            )
            .first()
        )


        if not investigation:
            raise HTTPException(
                status_code=404,
                detail="Investigation not found",
            )


        return {
            "id": investigation.id,
            "transaction_id": investigation.transaction_id,
            "risk_assessment": {
                "ml_score": investigation.ml_score,
                "rule_score": investigation.rule_score,
                "final_risk_score": investigation.final_risk_score,
                "risk_level": investigation.risk_level,
            },
            "confidence": investigation.confidence,
            "conclusion": investigation.ai_conclusion,
            "report": investigation.full_report_json,
            "created_at": investigation.created_at,
        }

    finally:
        session.close()