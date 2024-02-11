"""add_ru_title

Revision ID: c2b34fb2fed4
Revises: f4a13c357e31
Create Date: 2024-01-28 13:16:29.906066

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "c2b34fb2fed4"
down_revision = "f4a13c357e31"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product_category", sa.Column("ru_title", sa.String(), nullable=True))
    op.create_index(
        op.f("ix_product_category_ru_title"),
        "product_category",
        ["ru_title"],
        unique=True,
    )
    op.add_column(
        "product_composition", sa.Column("ru_title", sa.String(), nullable=True)
    )
    op.create_index(
        op.f("ix_product_composition_ru_title"),
        "product_composition",
        ["ru_title"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_product_composition_ru_title"), table_name="product_composition"
    )
    op.drop_column("product_composition", "ru_title")
    op.drop_index(op.f("ix_product_category_ru_title"), table_name="product_category")
    op.drop_column("product_category", "ru_title")
    # ### end Alembic commands ###
