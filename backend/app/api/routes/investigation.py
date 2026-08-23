from fastapi import APIRouter

from backend.app.investigation.llm_investigator import (
    investigate_transaction,
)


router = APIRouter(
    prefix="/api",
    tags=["Investigation"],
)


@router.get("/investigate/{transaction_id}")
def investigate(
    transaction_id: str,
):
    try:
        result = investigate_transaction(
            transaction_id
        )

        return {
            "status": "success",
            "data": result,
        }

    except ValueError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }