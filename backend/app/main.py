from fastapi import FastAPI
from sqlalchemy import text

from backend.app.db.database import engine
from backend.app.db.models import (
    Employee,
    Vendor,
    BankAccount,
    Invoice,
    Transaction,
    Approval,
    Incident,
)

from backend.app.api.routes.investigation import (
    router as investigation_router,
)

from backend.app.api.routes.history import (
    router as history_router,
)



app = FastAPI(
    title="AI Risk Investigator",
    description="AI-powered financial transaction risk investigation system",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-risk-investigator",
    }


@app.get("/health/database")
def database_health_check():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.scalar_one()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(exc),
        }


app.include_router(
    investigation_router
)

app.include_router(
    history_router
)