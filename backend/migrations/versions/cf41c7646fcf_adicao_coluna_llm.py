"""adicao_coluna_llm

Revision ID: cf41c7646fcf
Revises: c8ef4570badd
Create Date: 2026-05-09 03:56:32.771343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf41c7646fcf'
down_revision = 'c8ef4570badd'
branch_labels = None
depends_on = None

def upgrade():

    # remove FK antiga
    with op.batch_alter_table('materias', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_materias_llm_id',
            type_='foreignkey'
        )

    # remove PK antiga + altera tabela llm
    with op.batch_alter_table('llm', schema=None) as batch_op:

        # adiciona novas colunas
        batch_op.add_column(sa.Column('id', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('nome', sa.String(length=64), nullable=False))

        # remove coluna antiga
        batch_op.drop_column('model_id')

        # cria nova PK
        batch_op.create_primary_key('pk_llm', ['id'])

    # cria nova FK
    with op.batch_alter_table('materias', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_materias_llm_id',
            'llm',
            ['llm_id'],
            ['id']
        )


def downgrade():

    # remove FK nova
    with op.batch_alter_table('materias', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_materias_llm_id',
            type_='foreignkey'
        )

    # reverte tabela llm
    with op.batch_alter_table('llm', schema=None) as batch_op:

        # remove PK nova
        batch_op.drop_constraint('pk_llm', type_='primary')

        # recria coluna antiga
        batch_op.add_column(
            sa.Column('model_id', sa.VARCHAR(), nullable=False)
        )

        # remove novas colunas
        batch_op.drop_column('nome')
        batch_op.drop_column('id')

    # recria FK antiga
    with op.batch_alter_table('materias', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_materias_llm_id',
            'llm',
            ['llm_id'],
            ['model_id']
        )