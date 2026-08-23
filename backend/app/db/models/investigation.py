from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Float, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey(
            "transactions.transaction_id"
        ),
        nullable=False,
        index=True,
    )

    ml_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    rule_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    final_risk_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    confidence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    ai_conclusion: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    full_report_json: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )