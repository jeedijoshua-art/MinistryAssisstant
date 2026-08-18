"""Add GeneratedImage

Revision ID: 02650786c298
Revises: 1cd3feca8a84
Create Date: 2026-08-07 09:59:05.251520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02650786c298'
down_revision: Union[str, None] = '1cd3feca8a84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'generated_images',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('provider_model', sa.String(length=100), nullable=True),
        sa.Column('cloudinary_url', sa.String(length=512), nullable=True),
        sa.Column('generation_status', sa.String(length=50), nullable=False),
        sa.Column('conversation_id', sa.Uuid(), nullable=True),
        sa.Column('tool_name', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_images_conversation_id'), 'generated_images', ['conversation_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_generated_images_conversation_id'), table_name='generated_images')
    op.drop_table('generated_images')
