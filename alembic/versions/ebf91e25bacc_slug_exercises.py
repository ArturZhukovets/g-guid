"""slug_exercises

Revision ID: ebf91e25bacc
Revises: 87444ee07147
Create Date: 2023-09-24 00:35:00.545753

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "ebf91e25bacc"
down_revision = "87444ee07147"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("exercise", sa.Column("slug", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("exercise", "slug")
    # ### end Alembic commands ###
