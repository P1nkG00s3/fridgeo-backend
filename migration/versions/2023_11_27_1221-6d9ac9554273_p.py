"""p

Revision ID: 6d9ac9554273
Revises: 9d57daf7eebf
Create Date: 2023-11-27 12:21:42.100849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d9ac9554273'
down_revision: Union[str, None] = '9d57daf7eebf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
