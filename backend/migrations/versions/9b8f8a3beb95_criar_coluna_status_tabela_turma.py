"""criar_coluna_status_tabela_turma

Revision ID: 9b8f8a3beb95
Revises: 6ef7e1892623
Create Date: 2026-05-21 02:21:55.740641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b8f8a3beb95'
down_revision = '6ef7e1892623'
branch_labels = None
depends_on = None



def upgrade():
    with op.batch_alter_table('turmas', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'status',
                sa.Enum(
                    'ATIVO',
                    'INATIVO',
                    name='statusturmaenum',
                    native_enum=False
                ),
                nullable=False,
                server_default='ATIVO'
            )
        )


def downgrade():
    with op.batch_alter_table('turmas', schema=None) as batch_op:
        batch_op.drop_column('status')    
