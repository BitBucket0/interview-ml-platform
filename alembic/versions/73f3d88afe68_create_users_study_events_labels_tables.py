"""create users study_events labels tables

Revision ID: 73f3d88afe68
Revises: 
Create Date: 2026-05-26 18:44:16.948457

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "001_create_core_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    upgrade() applies the migration.

    This creates three tables:
    1. users
    2. study_events
    3. labels
    """

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    op.create_table(
        "study_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("topic_tag", sa.String(length=100), nullable=False),
        sa.Column("leetcode_id", sa.Integer(), nullable=True),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("minutes_spent", sa.Integer(), nullable=False),
        sa.Column("outcome", sa.String(length=100), nullable=False),
        sa.Column(
            "ts",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "ix_study_events_user_id",
        "study_events",
        ["user_id"],
    )

    op.create_index(
        "ix_study_events_topic_tag",
        "study_events",
        ["topic_tag"],
    )

    op.create_index(
        "ix_study_events_ts",
        "study_events",
        ["ts"],
    )

    op.create_table(
        "labels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("next_success_7d", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "ix_labels_user_id",
        "labels",
        ["user_id"],
    )


def downgrade() -> None:
    """
    downgrade() reverses the migration.

    Drop child tables first, then parent table.
    """

    op.drop_index("ix_labels_user_id", table_name="labels")
    op.drop_table("labels")

    op.drop_index("ix_study_events_ts", table_name="study_events")
    op.drop_index("ix_study_events_topic_tag", table_name="study_events")
    op.drop_index("ix_study_events_user_id", table_name="study_events")
    op.drop_table("study_events")

    op.drop_table("users")
