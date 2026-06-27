"""adiciona coluna status na tabela llm

Revision ID: a1b2c3d4e5f6
Revises: 63125fcdb5a0
Create Date: 2026-06-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '63125fcdb5a0'
branch_labels = None
depends_on = None


def upgrade():
    # A coluna `status` existe no model LLM (model_llm.py) desde a US-38, mas nenhuma
    # migração a criava — o schema migrado tinha apenas `id` e `nome`. Como o model
    # usa `native_enum=False`, é um VARCHAR simples (sem TYPE nativo no Postgres).
    # `server_default` garante o NOT NULL em linhas já existentes.
    op.add_column(
        'llm',
        sa.Column(
            'status',
            sa.Enum('ativada', 'desativada', name='llmstatusenum', native_enum=False),
            nullable=False,
            server_default='desativada',
        ),
    )


def downgrade():
    op.drop_column('llm', 'status')
