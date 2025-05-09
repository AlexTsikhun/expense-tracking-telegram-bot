"""Use more precise type to store money. Remove index from id (it does automatically). Make fields required, update date saving

Revision ID: 290ef128b806
Revises: b815d9360b78
Create Date: 2025-04-10 13:38:02.458476

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "290ef128b806"
down_revision: Union[str, None] = "b815d9360b78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("expenses", schema=None) as batch_op:
        batch_op.alter_column("title", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column(
            "amount_uah", existing_type=sa.FLOAT(), type_=sa.Numeric(precision=10, scale=2), nullable=False
        )
        batch_op.alter_column(
            "amount_usd", existing_type=sa.FLOAT(), type_=sa.Numeric(precision=10, scale=2), nullable=False
        )
        batch_op.drop_index("ix_expenses_id")
        batch_op.create_index(batch_op.f("ix_expenses_date"), ["date"], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("expenses", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_expenses_date"))
        batch_op.create_index("ix_expenses_id", ["id"], unique=False)
        batch_op.alter_column(
            "amount_usd", existing_type=sa.Numeric(precision=10, scale=2), type_=sa.FLOAT(), nullable=True
        )
        batch_op.alter_column(
            "amount_uah", existing_type=sa.Numeric(precision=10, scale=2), type_=sa.FLOAT(), nullable=True
        )
        batch_op.alter_column("title", existing_type=sa.VARCHAR(), nullable=True)

    # ### end Alembic commands ###
