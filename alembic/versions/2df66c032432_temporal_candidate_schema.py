"""temporal candidate schema

Revision ID: 2df66c032432
Revises: 001_create_core_tables
Create Date: 2026-07-06 12:38:18.356446
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2df66c032432'
down_revision: Union[str, None] = '001_create_core_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Canonical problem catalog
    op.create_table(
        "problems",
        sa.Column("id", sa.String(length=26), primary_key=True),
        sa.Column("leetcode_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("topic_tag", sa.String(length=100), nullable=False),
        sa.Column("difficulty", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("leetcode_id", name="uq_problems_leetcode_id"),
    )
    op.create_index(
        "ix_problems_active_topic_difficulty",
        "problems",
        ["topic_tag", "difficulty"],
        unique=False,
        postgresql_where=sa.text("is_active = true"),
    )
    # Decision points: one row = one moment where the system could make a recommendation
    op.create_table(
        "prediction_instances",
        sa.Column("id", sa.String(length=26), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("as_of_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("label_window_end_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("feature_set_version", sa.String(length=50), nullable=False),
        sa.Column("candidate_generation_version", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "as_of_ts", "source", name="uq_prediction_instances_user_asof_source"),
        sa.CheckConstraint(
            "label_window_end_ts = as_of_ts + interval '7 days'",
            name="ck_prediction_instances_label_window_7d",
        ),
    )

    op.create_index(
        "ix_prediction_instances_user_asof",
        "prediction_instances",
        ["user_id", "as_of_ts"],
    )
    op.create_index(
        "ix_prediction_instances_asof",
        "prediction_instances",
        ["as_of_ts"],
    )

    # Add problem_id to study_events.
    # Keep old leetcode_id/topic_tag/difficulty columns for now so this migration is not destructive.
    op.add_column("study_events", sa.Column("problem_id", sa.String(length=26), nullable=True))
    op.add_column(
        "study_events",
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_foreign_key(
        "fk_study_events_problem_id_problems",
        "study_events",
        "problems",
        ["problem_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_index("ix_study_events_problem_id", "study_events", ["problem_id"])

def downgrade() -> None:
    op.drop_index("ix_study_events_problem_id", table_name="study_events")
    op.drop_constraint(
        "fk_study_events_problem_id_problems",
        "study_events",
        type_="foreignkey",
    )
    op.drop_column("study_events", "ingested_at")
    op.drop_column("study_events", "problem_id")

    op.drop_index(
        "ix_prediction_instances_asof",
        table_name="prediction_instances",
    )
    op.drop_index(
        "ix_prediction_instances_user_asof",
        table_name="prediction_instances",
    )
    op.drop_table("prediction_instances")

    op.drop_index(
        "ix_problems_active_topic_difficulty",
        table_name="problems",
    )
    op.drop_table("problems")