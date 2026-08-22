from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    vendor_id: Mapped[str] = mapped_column(
        ForeignKey("vendors.vendor_id"),
        nullable=False,
        index=True,
    )

    invoice_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    invoice_amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    invoice_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )

    vendor: Mapped["Vendor"] = relationship(
        back_populates="invoices",
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="invoice",
    )