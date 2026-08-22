from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    vendor_id: Mapped[str] = mapped_column(
        ForeignKey("vendors.vendor_id"),
        nullable=False,
        index=True,
    )

    employee_id: Mapped[str] = mapped_column(
        ForeignKey("employees.employee_id"),
        nullable=False,
        index=True,
    )

    bank_account_id: Mapped[str] = mapped_column(
        ForeignKey("bank_accounts.account_id"),
        nullable=False,
        index=True,
    )

    location: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    invoice_id: Mapped[str] = mapped_column(
        ForeignKey("invoices.invoice_id"),
        nullable=False,
        index=True,
    )

    approval_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )

    vendor: Mapped["Vendor"] = relationship(
        back_populates="transactions",
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="transactions",
    )

    bank_account: Mapped["BankAccount"] = relationship(
        back_populates="transactions",
    )

    invoice: Mapped["Invoice"] = relationship(
        back_populates="transactions",
    )

    approvals: Mapped[list["Approval"]] = relationship(
        back_populates="transaction",
    )