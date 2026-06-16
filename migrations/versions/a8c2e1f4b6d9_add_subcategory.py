"""add subcategory to transaction

Revision ID: a8c2e1f4b6d9
Revises: 0973d46897bf
Create Date: 2026-06-16

"""
from alembic import op
import sqlalchemy as sa

revision = 'a8c2e1f4b6d9'
down_revision = '0973d46897bf'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subcategory', sa.String(length=40), nullable=True))


def downgrade():
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_column('subcategory')
