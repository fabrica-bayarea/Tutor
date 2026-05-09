"""add token_convite table

Revision ID: ed8be2427b8b
Revises: 7487a1a7e894
Create Date: 2026-05-08 23:28:27.070057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed8be2427b8b'
down_revision = 'cf41c7646fcf'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('token_convite',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(length=36), nullable=False),
    sa.Column('usuario_id', sa.UUID(), nullable=False),
    sa.Column('used', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('token_convite', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_convite_token'), ['token'], unique=True)

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column(          # <-- alter_column, não add_column
            'status',
            existing_type=sa.Enum('Ativo', 'Inativo', native_enum=False),
            type_=sa.Enum('ADMIN', 'PROFESSOR', 'ALUNO', 'ATIVO', 'INATIVO',
                          name='roleenum', native_enum=False),
            existing_nullable=False,
            server_default='ATIVO'
        )


def downgrade():
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column(          # <-- revertendo para o tipo original
            'status',
            existing_type=sa.Enum('ADMIN', 'PROFESSOR', 'ALUNO', 'ATIVO', 'INATIVO',
                                  name='roleenum', native_enum=False),
            type_=sa.Enum('Ativo', 'Inativo', native_enum=False),
            existing_nullable=False
        )

    with op.batch_alter_table('token_convite', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_convite_token'))

    op.drop_table('token_convite')