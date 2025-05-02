"""
Serviço dedicado a lidar com vínculos nas entidades intermediárias, como 'AlunoTurma', 'ArquivoTurmaMateria', etc.
"""

import uuid
from application.config import db
from application.models import AlunoTurma, ProfessorTurmaMateria, ArquivoTurmaMateria

# -------------------- ALUNO <-> TURMA --------------------

def buscar_vinculos_aluno_turma(aluno_id: uuid.UUID = None, turma_id: uuid.UUID = None) -> list[AlunoTurma]:
    """
    Busca vínculos entre alunos e turmas baseado em um ou ambos os parâmetros.

    Espera receber um desses dois parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `turma_id`: uuid.UUID - o ID da turma

    Retorna uma lista de vínculos AlunoTurma que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    if not aluno_id and not turma_id:
        return None
    
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

# -------------------- PROFESSOR <-> TURMA <-> MATÉRIA --------------------

def buscar_vinculos_professor_turma_materia(professor_id: uuid.UUID = None, turma_id: uuid.UUID = None, materia_id: uuid.UUID = None) -> list[ProfessorTurmaMateria]:
    """
    Busca vínculos entre professores, turmas e matérias baseado em um ou todos os parâmetros.

    Espera receber um desses três parâmetros:
    - `professor_id`: uuid.UUID - o ID do professor
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna uma lista de vínculos ProfessorTurmaMateria que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    if not professor_id and not turma_id and not materia_id:
        return None
    
    query = ProfessorTurmaMateria.query

    if professor_id is not None:
        query = query.filter_by(professor_id=professor_id)
    
    if turma_id is not None:
        query = query.filter_by(turma_id=turma_id)
    
    if materia_id is not None:
        query = query.filter_by(materia_id=materia_id)
    
    return query.all()

def criar_vinculo_professor_turma_materia(professor_id: uuid.UUID, turma_id: uuid.UUID, materia_id: uuid.UUID) -> bool:
    """
    Cria um novo vínculo entre um professor, uma turma e uma matéria.

    Espera receber:
    - `professor_id`: uuid.UUID - o ID do professor
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    existe = buscar_vinculo_professor_turma_materia(professor_id, turma_id, materia_id)
    if existe:
        return False
    
    db.session.add(ProfessorTurmaMateria(professor_id=professor_id, turma_id=turma_id, materia_id=materia_id))
    db.session.commit()
    return True
