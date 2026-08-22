from __future__ import annotations
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    company_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    industry: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    bank_account_id: Mapped[str] = mapped_column(
        ForeignKey("bank_accounts.account_id"),
        nullable=False,
        index=True,
    )

    risk_history: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="none",
    )

    bank_account: Mapped["BankAccount"] = relationship(
        back_populates="vendors",
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="vendor",
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="vendor",
    )