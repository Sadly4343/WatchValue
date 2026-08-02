
"""initial tables

Revision ID: 0bc9623887fa
Revises: 
Create Date: 2026-08-02
"""
from collections.abc import Sequence

import pgvector.sqlalchemy
import sqlalchemy as sa

from alembic import op

revision: str = '0bc9623887fa'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    op.create_table(
        'document_chunks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_type', sa.String(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('chunk_text', sa.Text(), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=1536), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_chunks_id'), 'document_chunks', ['id'], unique=False)

    op.create_table(
        'listings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('manufacturer', sa.String(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('grade', sa.String(), nullable=True),
        sa.Column('size', sa.String(), nullable=True),
        sa.Column('jewels', sa.Integer(), nullable=True),
        sa.Column('case_material', sa.String(), nullable=True),
        sa.Column('case_maker', sa.String(), nullable=True),
        sa.Column('running_condition', sa.String(), nullable=True),
        sa.Column('original_dial', sa.Boolean(), nullable=True),
        sa.Column('original_hands', sa.Boolean(), nullable=True),
        sa.Column('case_condition_notes', sa.Text(), nullable=True),
        sa.Column('sold_price', sa.Numeric(), nullable=False),
        sa.Column('sold_date', sa.Date(), nullable=False),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('listing_url', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_listings_id'), 'listings', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_listings_id'), table_name='listings')
    op.drop_table('listings')
    op.drop_index(op.f('ix_document_chunks_id'), table_name='document_chunks')
    op.drop_table('document_chunks')
