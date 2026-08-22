from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    account_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    bank_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    account_number_masked: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    owner_entity: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    vendors: Mapped[list["Vendor"]] = relationship(
        back_populates="bank_account",
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="bank_account",
    )