"""add created timestamp default to investigations

Revision ID: 913f1d8f1d4c
Revises: 9f70829e6a3d
Create Date: 2026-08-23 08:18:48.923998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '913f1d8f1d4c'
down_revision: Union[str, Sequence[str], None] = '9f70829e6a3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "investigations",
        "created_at",
        server_default=sa.text("now()"),
        existing_type=sa.DateTime(),
        nullable=False,
    )

def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "investigations",
        "created_at",
        server_default=None,
        existing_type=sa.DateTime(),
        nullable=False,
    )