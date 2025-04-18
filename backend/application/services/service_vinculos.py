"""
Serviço dedicado a lidar com vínculos nas entidades intermediárias, como 'AlunoTurma', 'ArquivoTurmaMateria', etc.
"""

import uuid
from application.config import db
from application.models import AlunoTurma, ProfessorTurma, ProfessorMateria, TurmaMateria, ArquivoTurmaMateria

# -------------------- ALUNO <-> TURMA --------------------

def buscar_vinculos_aluno_turma(aluno_id: uuid.UUID = None, turma_id: uuid.UUID = None) -> list[AlunoTurma]:
    """
    Busca vínculos entre alunos e turmas baseado em um ou ambos os parâmetros.

    Espera receber um desses dois parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `turma_id`: uuid.UUID - o ID da turma

    Retorna uma lista de vínculos AlunoTurma que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna todos os vínculos.
    """
    query = AlunoTurma.query

    if aluno_id is not None:
        query = query.filter_by(aluno_id=aluno_id)
    
    if turma_id is not None:
        query = query.filter_by(turma_id=turma_id)
    
    return query.all()

def criar_vinculo_aluno_turma(aluno_id: uuid.UUID, turma_id: uuid.UUID) -> bool:
    """
    Cria um novo vínculo entre um aluno e uma turma.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `turma_id`: uuid.UUID - o ID da turma

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    existe = buscar_vinculo_aluno_turma(aluno_id, turma_id)
    if existe:
        return False
    
    db.session.add(AlunoTurma(aluno_id=aluno_id, turma_id=turma_id))
    db.session.commit()
    return True
