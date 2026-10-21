"""Create the equipment table."""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "equipment",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(),
            nullable=False,
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("location", sa.String(100), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.true(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    # Reversing this migration deletes the table and its rows.
    op.drop_table("equipment")