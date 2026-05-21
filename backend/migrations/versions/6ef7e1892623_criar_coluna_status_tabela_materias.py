"""criar_coluna_status_tabela_materias

Revision ID: 6ef7e1892623
Revises: f84352a987bc
Create Date: 2026-05-21 00:34:17.221119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ef7e1892623'
down_revision = 'f84352a987bc'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('materias', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'status',
                sa.Enum(
                    'ATIVO',
                    'INATIVO',
                    name='statusmateriaenum',
                    native_enum=False
                ),
                nullable=False,
                server_default='ATIVO'
            )
        )


def downgrade():
    with op.batch_alter_table('materias', schema=None) as batch_op:
        batch_op.drop_column('status')