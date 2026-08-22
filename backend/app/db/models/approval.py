from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    approval_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        ForeignKey("transactions.transaction_id"),
        nullable=False,
        index=True,
    )

    employee_id: Mapped[str] = mapped_column(
        ForeignKey("employees.employee_id"),
        nullable=False,
        index=True,
    )

    approval_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    transaction: Mapped["Transaction"] = relationship(
        back_populates="approvals",
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="approvals",
    )