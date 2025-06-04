"""
Serviço dedicado a lidar com vínculos nas entidades intermediárias, como 'AlunoTurma', 'ArquivoTurmaMateria', etc.
"""

import uuid
from application.config import db
from application.models import AlunoTurma, ProfessorTurmaMateria, ArquivoTurmaMateria

# -------------------- ALUNO <-> TURMA --------------------

def buscar_vinculos_aluno_turma(aluno_id: uuid.UUID = None, turma_id: uuid.UUID = None) -> list[AlunoTurma]:
    """
    Busca vínculos entre alunos e turmas.

    Espera receber um ou ambos esses dois parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `turma_id`: uuid.UUID - o ID da turma

    Retorna uma lista de vínculos AlunoTurma que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
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

    Espera receber todos esses dois parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `turma_id`: uuid.UUID - o ID da turma

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    if not aluno_id or not turma_id:
        raise ValueError("É obrigatório fornecer um ID de aluno e um ID de turma.")
    
    existe = buscar_vinculo_aluno_turma(aluno_id, turma_id)
    if existe:
        return False
    
    db.session.add(AlunoTurma(aluno_id=aluno_id, turma_id=turma_id))
    db.session.commit()
    return True

# -------------------- PROFESSOR <-> TURMA <-> MATÉRIA --------------------

def buscar_vinculos_professor_turma_materia(professor_id: uuid.UUID = None, turma_id: uuid.UUID = None, materia_id: uuid.UUID = None) -> list[ProfessorTurmaMateria]:
    """
    Busca vínculos entre professores, turmas e matérias.

    Espera receber um, dois ou todos esses três parâmetros:
    - `professor_id`: uuid.UUID - o ID do professor
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna uma lista de vínculos ProfessorTurmaMateria que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    query = ProfessorTurmaMateria.query
    
    if professor_id is not None:
        query = query.filter_by(professor_id=professor_id)
    
    if turma_id is not None:
        query = query.filter_by(turma_id=turma_id)
    
    if materia_id is not None:
        query = query.filter_by(materia_id=materia_id)
    
    return query.all()

def criar_vinculo_professor_turma_materia(professor_id: uuid.UUID, turma_id: uuid.UUID, materia_id: uuid.UUID) -> ProfessorTurmaMateria | None:
    """
    Cria um novo vínculo entre um professor, uma turma e uma matéria.

    Espera receber todos esses três parâmetros:
    - `professor_id`: uuid.UUID - o ID do professor
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna o novo vínculo se ele for criado com sucesso, e None se o vínculo já existir.
    """
    if not professor_id or not turma_id or not materia_id:
        raise ValueError("É obrigatório fornecer um ID de professor, um ID de turma e um ID de matéria.")
    
    existe = buscar_vinculo_professor_turma_materia(professor_id, turma_id, materia_id)
    if existe:
        return None
    
    novo_vinculo = ProfessorTurmaMateria(professor_id=professor_id, turma_id=turma_id, materia_id=materia_id)
    db.session.add(novo_vinculo)
    db.session.commit()
    return novo_vinculo

# -------------------- ARQUIVO <-> TURMA <-> MATÉRIA --------------------

def buscar_vinculos_arquivo_turma_materia(arquivo_id: uuid.UUID = None, turma_id: uuid.UUID = None, materia_id: uuid.UUID = None) -> list[ArquivoTurmaMateria]:
    """
    Busca vínculos entre arquivos, turmas e matérias.

    Espera receber um, dois ou todos esses três parâmetros:
    - `arquivo_id`: uuid.UUID - o ID do arquivo
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna uma lista de vínculos ArquivoTurmaMateria que correspondem aos filtros.
    Se nenhum parâmetro for fornecido, retorna None.
    """
    query = ArquivoTurmaMateria.query
    
    if arquivo_id is not None:
        query = query.filter_by(arquivo_id=arquivo_id)
    
    if turma_id is not None:
        query = query.filter_by(turma_id=turma_id)
    
    if materia_id is not None:
        query = query.filter_by(materia_id=materia_id)
    
    return query.all()

def criar_vinculo_arquivo_turma_materia(arquivo_id: uuid.UUID, turma_id: uuid.UUID, materia_id: uuid.UUID) -> ArquivoTurmaMateria | None:
    """
    Cria um novo vínculo entre um arquivo, uma turma e uma matéria.

    Espera receber todos esses três parâmetros:
    - `arquivo_id`: uuid.UUID - o ID do arquivo
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna o vínculo criado se ele for criado com sucesso, e None se o vínculo já existir.
    """
    if not arquivo_id or not turma_id or not materia_id:
        raise ValueError("É obrigatório fornecer um ID de arquivo, um ID de turma e um ID de matéria.")
    
    existe = buscar_vinculos_arquivo_turma_materia(arquivo_id, turma_id, materia_id)
    if existe:
        return None
    
    novo_vinculo = ArquivoTurmaMateria(arquivo_id=arquivo_id, turma_id=turma_id, materia_id=materia_id)
    db.session.add(novo_vinculo)
    db.session.commit()
    return novo_vinculo
