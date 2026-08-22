from __future__ import annotations
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class Employee(Base):
    __tablename__ = "employees"

    employee_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    authorization_limit: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="employee",
    )

    approvals: Mapped[list["Approval"]] = relationship(
        back_populates="employee",
    )