"""adiciona coluna nome na tabela llm

Revision ID: 63125fcdb5a0
Revises: 9b8f8a3beb95
Create Date: 2026-05-21 23:54:30.951999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63125fcdb5a0'
down_revision = '9b8f8a3beb95'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('llm', schema=None) as batch_op:
        batch_op.alter_column('model_id', new_column_name='id')
        batch_op.add_column(sa.Column('nome', sa.String(length=64), nullable=True))


def downgrade():
    with op.batch_alter_table('llm', schema=None) as batch_op:
        batch_op.drop_column('nome')
        batch_op.alter_column('id', new_column_name='model_id')