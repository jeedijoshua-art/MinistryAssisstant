"""initial foundation schema and default ministry data

Revision ID: 20260719_0001
Revises:
Create Date: 2026-07-19
"""
from alembic import op
from sqlalchemy import text
from app.database.base import Base
import app.models  # noqa: F401

revision = "20260719_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
    Base.metadata.create_all(bind=bind)
    bind.execute(text("""
        INSERT INTO churches (id, name, primary_theme, accent, created_at, updated_at)
        VALUES (gen_random_uuid(), 'ZION PRAYER TOWER', 'Dark Blue', 'Gold', now(), now())
        ON CONFLICT (name) DO NOTHING
    """))


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
