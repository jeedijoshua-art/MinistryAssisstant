"""Add Bible Engine models

Revision ID: b688031139ce
Revises: 20260719_0001
Create Date: 2026-07-19 18:53:32.860143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b688031139ce'
down_revision: Union[str, None] = '20260719_0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
