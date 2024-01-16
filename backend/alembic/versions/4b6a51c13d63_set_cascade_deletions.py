"""set cascade deletions

Revision ID: 4b6a51c13d63
Revises: 1fe9ebec49bf
Create Date: 2023-12-24 15:07:37.921269

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "4b6a51c13d63"
down_revision = "1fe9ebec49bf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "user_subscription_coach_id_fkey", "user_subscription", type_="foreignkey"
    )
    op.drop_constraint(
        "user_subscription_owner_id_fkey", "user_subscription", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "user_subscription", "user", ["owner_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "user_subscription", "user", ["coach_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user_subscription", type_="foreignkey")
    op.drop_constraint(None, "user_subscription", type_="foreignkey")
    op.create_foreign_key(
        "user_subscription_owner_id_fkey",
        "user_subscription",
        "user",
        ["owner_id"],
        ["id"],
    )
    op.create_foreign_key(
        "user_subscription_coach_id_fkey",
        "user_subscription",
        "user",
        ["coach_id"],
        ["id"],
    )
    # ### end Alembic commands ###
