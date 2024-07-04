"""create extraction_jobs table

Revision ID: 18b782c4ed76
Revises: 
Create Date: 2024-07-04 00:21:03.117211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18b782c4ed76'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
