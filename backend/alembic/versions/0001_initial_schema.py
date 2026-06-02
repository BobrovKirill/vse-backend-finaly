"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-01
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "health_indicators",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_health_indicators_code"), "health_indicators", ["code"], unique=True)
    op.create_index(op.f("ix_health_indicators_id"), "health_indicators", ["id"], unique=False)

    op.create_table(
        "packages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("included_services", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_packages_id"), "packages", ["id"], unique=False)

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("help_text", sa.Text(), nullable=True),
        sa.Column("question_type", sa.String(length=20), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_questions_id"), "questions", ["id"], unique=False)

    op.create_table(
        "answers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_answers_id"), "answers", ["id"], unique=False)

    op.create_table(
        "answer_effects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("answer_id", sa.Integer(), nullable=False),
        sa.Column("indicator_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["answer_id"], ["answers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["indicator_id"], ["health_indicators.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("answer_id", "indicator_id"),
    )
    op.create_index(op.f("ix_answer_effects_id"), "answer_effects", ["id"], unique=False)

    op.create_table(
        "package_rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("package_id", sa.Integer(), nullable=False),
        sa.Column("indicator_id", sa.Integer(), nullable=False),
        sa.Column("min_score", sa.Integer(), nullable=False),
        sa.Column("max_score", sa.Integer(), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["indicator_id"], ["health_indicators.id"]),
        sa.ForeignKeyConstraint(["package_id"], ["packages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("package_id", "indicator_id"),
    )
    op.create_index(op.f("ix_package_rules_id"), "package_rules", ["id"], unique=False)

    op.create_table(
        "choices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contact_name", sa.String(length=255), nullable=True),
        sa.Column("contact_phone", sa.String(length=64), nullable=True),
        sa.Column("recommended_package_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["recommended_package_id"], ["packages.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_choices_id"), "choices", ["id"], unique=False)

    op.create_table(
        "choices_answers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("choice_id", sa.Integer(), nullable=False),
        sa.Column("answer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["answer_id"], ["answers.id"]),
        sa.ForeignKeyConstraint(["choice_id"], ["choices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_choices_answers_id"), "choices_answers", ["id"], unique=False)

    op.create_table(
        "choices_indicator_scores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("choice_id", sa.Integer(), nullable=False),
        sa.Column("indicator_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["choice_id"], ["choices.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["indicator_id"], ["health_indicators.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("choice_id", "indicator_id"),
    )
    op.create_index(op.f("ix_choices_indicator_scores_id"), "choices_indicator_scores", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_choices_indicator_scores_id"), table_name="choices_indicator_scores")
    op.drop_table("choices_indicator_scores")
    op.drop_index(op.f("ix_choices_answers_id"), table_name="choices_answers")
    op.drop_table("choices_answers")
    op.drop_index(op.f("ix_choices_id"), table_name="choices")
    op.drop_table("choices")
    op.drop_index(op.f("ix_package_rules_id"), table_name="package_rules")
    op.drop_table("package_rules")
    op.drop_index(op.f("ix_answer_effects_id"), table_name="answer_effects")
    op.drop_table("answer_effects")
    op.drop_index(op.f("ix_answers_id"), table_name="answers")
    op.drop_table("answers")
    op.drop_index(op.f("ix_questions_id"), table_name="questions")
    op.drop_table("questions")
    op.drop_index(op.f("ix_packages_id"), table_name="packages")
    op.drop_table("packages")
    op.drop_index(op.f("ix_health_indicators_id"), table_name="health_indicators")
    op.drop_index(op.f("ix_health_indicators_code"), table_name="health_indicators")
    op.drop_table("health_indicators")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
