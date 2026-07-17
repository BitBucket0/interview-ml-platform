"""add training examples

Revision ID: a6aef06e35cc
Revises: 2df66c032432
Create Date: 2026-07-17 17:01:30.124848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6aef06e35cc'
down_revision: Union[str, None] = '2df66c032432'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
