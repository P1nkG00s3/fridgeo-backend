"""empty message

Revision ID: db48ac7eec4d
Revises: 936ca8e59b95
Create Date: 2023-10-30 11:24:25.579214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db48ac7eec4d'
down_revision: Union[str, None] = '936ca8e59b95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('name', sa.String(), nullable=False))
    op.drop_column('role', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('role', 'name')
    # ### end Alembic commands ###