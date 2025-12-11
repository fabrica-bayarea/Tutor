def upgrade():
    # Criação de nova tabela 'usuario'
    op.create_table(
        'usuario',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('matricula', sa.String(length=10), nullable=False),
        sa.Column('nome', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=64), nullable=False),
        sa.Column('senha', sa.String(length=128), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'PROFESSOR', 'ALUNO', name='roleenum'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_usuario_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_usuario_matricula'), ['matricula'], unique=True)

    # Criação de tabela 'sessao'
    op.create_table(
        'sessao',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('dono_id', sa.UUID(), nullable=False),
        sa.Column('inicio', sa.Date(), nullable=False),
        sa.Column('fim', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['dono_id'], ['usuario.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Atualização das tabelas dependentes antes de dropar 'alunos'
    with op.batch_alter_table('alunos_turmas', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('alunos_turmas_aluno_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'usuario', ['aluno_id'], ['id'])

    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('chats_aluno_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'usuario', ['aluno_id'], ['id'])

    # Atualização de professores e arquivos
    with op.batch_alter_table('arquivos', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('arquivos_professor_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'usuario', ['professor_id'], ['id'])

    with op.batch_alter_table('professores_turmas_materias', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('professores_turmas_materias_professor_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'usuario', ['professor_id'], ['id'])

    # Agora é seguro dropar 'alunos' e 'professores'
    with op.batch_alter_table('alunos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_alunos_cpf'))
        batch_op.drop_index(batch_op.f('ix_alunos_email'))
        batch_op.drop_index(batch_op.f('ix_alunos_matricula'))
    op.drop_table('alunos')

    with op.batch_alter_table('professores', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_professores_cpf'))
        batch_op.drop_index(batch_op.f('ix_professores_email'))
        batch_op.drop_index(batch_op.f('ix_professores_matricula'))
    op.drop_table('professores')

    # Alterações finais na tabela 'chats' e 'mensagens'
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('materia_id', sa.UUID(), nullable=False))
        batch_op.create_foreign_key(None, 'materias', ['materia_id'], ['id'])

    with op.batch_alter_table('mensagens', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sessao_id', sa.UUID(), nullable=False))
        batch_op.drop_constraint(batch_op.f('mensagens_chat_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'sessao', ['sessao_id'], ['id'])
        batch_op.drop_column('chat_id')
