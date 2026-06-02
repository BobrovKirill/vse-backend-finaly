"""package catalog and recommendations

Revision ID: 0002_package_catalog
Revises: 0001_initial_schema
Create Date: 2026-06-01
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_package_catalog"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("answers", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("packages", sa.Column("checkout_url", sa.String(length=2048), nullable=True))

    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_services_id"), "services", ["id"], unique=False)

    op.create_table(
        "packages_services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("package_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["package_id"], ["packages.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("package_id", "service_id"),
    )
    op.create_index(op.f("ix_packages_services_id"), "packages_services", ["id"], unique=False)

    op.execute(
        """
        INSERT INTO services (title, description, price, is_active)
        SELECT 'Состав пакета #' || id, included_services, NULL, TRUE
        FROM packages
        WHERE included_services IS NOT NULL AND included_services <> ''
        """
    )
    op.execute(
        """
        INSERT INTO packages_services (package_id, service_id, position)
        SELECT packages.id, services.id, 0
        FROM packages
        JOIN services ON services.title = 'Состав пакета #' || packages.id
        """
    )
    op.drop_column("packages", "included_services")

    op.create_table(
        "choices_package_recommendations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("choice_id", sa.Integer(), nullable=False),
        sa.Column("package_id", sa.Integer(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("matched_weight", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["choice_id"], ["choices.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["package_id"], ["packages.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("choice_id", "package_id"),
        sa.UniqueConstraint("choice_id", "rank"),
    )
    op.create_index(
        op.f("ix_choices_package_recommendations_id"),
        "choices_package_recommendations",
        ["id"],
        unique=False,
    )
    op.execute(
        """
        INSERT INTO choices_package_recommendations (choice_id, package_id, rank, matched_weight)
        SELECT id, recommended_package_id, 1, 0
        FROM choices
        WHERE recommended_package_id IS NOT NULL
        """
    )
    op.drop_constraint("choices_recommended_package_id_fkey", "choices", type_="foreignkey")
    op.drop_column("choices", "recommended_package_id")


def downgrade() -> None:
    op.add_column("choices", sa.Column("recommended_package_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "choices_recommended_package_id_fkey",
        "choices",
        "packages",
        ["recommended_package_id"],
        ["id"],
    )
    op.execute(
        """
        UPDATE choices
        SET recommended_package_id = recommendations.package_id
        FROM choices_package_recommendations AS recommendations
        WHERE recommendations.choice_id = choices.id AND recommendations.rank = 1
        """
    )
    op.drop_index(
        op.f("ix_choices_package_recommendations_id"),
        table_name="choices_package_recommendations",
    )
    op.drop_table("choices_package_recommendations")

    op.add_column("packages", sa.Column("included_services", sa.Text(), nullable=True))
    op.execute(
        """
        UPDATE packages
        SET included_services = package_services.description
        FROM (
            SELECT packages_services.package_id, string_agg(services.title, ', ' ORDER BY packages_services.position) AS description
            FROM packages_services
            JOIN services ON services.id = packages_services.service_id
            GROUP BY packages_services.package_id
        ) AS package_services
        WHERE packages.id = package_services.package_id
        """
    )
    op.execute("UPDATE packages SET included_services = '' WHERE included_services IS NULL")
    op.alter_column("packages", "included_services", nullable=False)
    op.drop_index(op.f("ix_packages_services_id"), table_name="packages_services")
    op.drop_table("packages_services")
    op.drop_index(op.f("ix_services_id"), table_name="services")
    op.drop_table("services")

    op.drop_column("packages", "checkout_url")
    op.drop_column("answers", "description")
