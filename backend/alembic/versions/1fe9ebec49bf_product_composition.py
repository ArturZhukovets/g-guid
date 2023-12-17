"""product composition

Revision ID: 1fe9ebec49bf
Revises: 99bc1c4e8e08
Create Date: 2023-12-17 15:47:55.433258

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "1fe9ebec49bf"
down_revision = "99bc1c4e8e08"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product_category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_product_category_id"), "product_category", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_product_category_title"), "product_category", ["title"], unique=True
    )
    op.create_table(
        "product_composition",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=True),
        sa.Column("update_date", sa.DateTime(), nullable=True),
        sa.Column("calories", sa.Float(), nullable=False),
        sa.Column("proteins", sa.Float(), nullable=False),
        sa.Column("fat", sa.Float(), nullable=False),
        sa.Column("carbohydrates", sa.Float(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["product_category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_product_composition_id"), "product_composition", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_product_composition_title"),
        "product_composition",
        ["title"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_product_composition_title"), table_name="product_composition"
    )
    op.drop_index(op.f("ix_product_composition_id"), table_name="product_composition")
    op.drop_table("product_composition")
    op.drop_index(op.f("ix_product_category_title"), table_name="product_category")
    op.drop_index(op.f("ix_product_category_id"), table_name="product_category")
    op.drop_table("product_category")
    # ### end Alembic commands ###
