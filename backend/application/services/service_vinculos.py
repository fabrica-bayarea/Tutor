"""
Serviço dedicado a lidar com operações CRUD relevantes para vínculos em tabelas intermediárias.
"""
import uuid
from application.config.database import db
from application.models import AlunoTurma, TurmaMateria, ProfessorTurmaMateria, ArquivoTurmaMateria

# -------------------- ALUNO <-> TURMA --------------------

def buscar_vinculos_aluno_turma(aluno_id: uuid.UUID = None, turma_id: uuid.UUID = None) -> list[dict]:
    """
    Busca vínculos entre alunos e turmas.

    Espera receber um ou ambos esses dois parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `turma_id`: uuid.UUID - o ID da turma

    Retorna uma lista de dicionários com vínculos AlunoTurma que correspondem aos filtros, e None se nada for encontrado.
    """
    if not aluno_id or not turma_id:
        raise ValueError("É obrigatório fornecer um ID de aluno e/ou um ID de turma.")
    
    vinculos = AlunoTurma.query
    
    if aluno_id is not None:
        vinculos = vinculos.filter_by(aluno_id=aluno_id)
    
    if turma_id is not None:
        vinculos = vinculos.filter_by(turma_id=turma_id)
    
    return [vinculo.to_dict() for vinculo in vinculos.all()] if vinculos else None

def criar_vinculo_aluno_turma(aluno_id: uuid.UUID, turma_id: uuid.UUID) -> bool:
    """
    Cria um novo vínculo entre um aluno e uma turma.

    Espera receber todos esses dois parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `turma_id`: uuid.UUID - o ID da turma

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    existe = buscar_vinculos_aluno_turma(aluno_id, turma_id)
    if existe:
        return False
    
    db.session.add(AlunoTurma(aluno_id=aluno_id, turma_id=turma_id))
    db.session.commit()
    return True

# -------------------- TURMA <-> MATÉRIA --------------------

def buscar_vinculos_turma_materia(turma_id: uuid.UUID = None, materia_id: uuid.UUID = None) -> list[dict]:
    """
    Busca vínculos entre turmas e matérias.

    Espera receber um ou ambos esses dois parâmetros:
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna uma lista de dicionários com vínculos TurmaMateria que correspondem aos filtros, e None se nada for encontrado.
    """
    if not turma_id or not materia_id:
        raise ValueError("É obrigatório fornecer um ID de turma e/ou um ID de matéria.")
    
    vinculos = TurmaMateria.query
    
    if turma_id is not None:
        vinculos = vinculos.filter_by(turma_id=turma_id)
    
    if materia_id is not None:
        vinculos = vinculos.filter_by(materia_id=materia_id)
    
    return [vinculo.to_dict() for vinculo in vinculos.all()] if vinculos else None

def criar_vinculo_turma_materia(turma_id: uuid.UUID, materia_id: uuid.UUID) -> bool:
    """
    Cria um novo vínculo entre uma turma e uma matéria.

    Espera receber todos esses dois parâmetros:
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna True se o vínculo for criado com sucesso, e False se o vínculo já existir.
    """
    existe = buscar_vinculos_turma_materia(turma_id, materia_id)
    if existe:
        return False
    
    db.session.add(TurmaMateria(turma_id=turma_id, materia_id=materia_id))
    db.session.commit()
    return True

# -------------------- PROFESSOR <-> TURMA <-> MATÉRIA --------------------

def buscar_vinculos_professor_turma_materia(professor_id: uuid.UUID = None, turma_id: uuid.UUID = None, materia_id: uuid.UUID = None) -> list[dict] | None:
    """
    Busca vínculos entre professores, turmas e matérias.

    Espera receber um, dois ou todos esses três parâmetros:
    - `professor_id`: uuid.UUID - o ID do professor
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna uma lista de dicionários com vínculos ProfessorTurmaMateria que correspondem aos filtros, e None se nada for encontrado.
    """
    if not professor_id or not turma_id or not materia_id:
        raise ValueError("É obrigatório fornecer um ID de professor e/ou um ID de turma e/ou um ID de matéria.")
    
    vinculos = ProfessorTurmaMateria.query
    
    if professor_id is not None:
        vinculos = vinculos.filter_by(professor_id=professor_id)
    
    if turma_id is not None:
        vinculos = vinculos.filter_by(turma_id=turma_id)
    
    if materia_id is not None:
        vinculos = vinculos.filter_by(materia_id=materia_id)
    
    return [vinculo.to_dict() for vinculo in vinculos.all()] if vinculos else None

def criar_vinculo_professor_turma_materia(professor_id: uuid.UUID, turma_id: uuid.UUID, materia_id: uuid.UUID) -> ProfessorTurmaMateria | None:
    """
    Cria um novo vínculo entre um professor, uma turma e uma matéria.

    Espera receber todos esses três parâmetros:
    - `professor_id`: uuid.UUID - o ID do professor
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna o novo vínculo se ele for criado com sucesso, e None se o vínculo já existir.
    """
    existe = buscar_vinculos_professor_turma_materia(professor_id, turma_id, materia_id)
    if existe:
        return None
    
    novo_vinculo = ProfessorTurmaMateria(professor_id=professor_id, turma_id=turma_id, materia_id=materia_id)
    db.session.add(novo_vinculo)
    db.session.commit()
    return novo_vinculo

# -------------------- ARQUIVO <-> TURMA <-> MATÉRIA --------------------

def buscar_vinculos_arquivo_turma_materia(arquivo_id: uuid.UUID = None, turma_id: uuid.UUID = None, materia_id: uuid.UUID = None) -> list[dict] | None:
    """
    Busca vínculos entre arquivos, turmas e matérias.

    Espera receber um, dois ou todos esses três parâmetros:
    - `arquivo_id`: uuid.UUID - o ID do arquivo
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna uma lista de dicionários com vínculos ArquivoTurmaMateria que correspondem aos filtros, e None se nada for encontrado.
    """
    if not arquivo_id or not turma_id or not materia_id:
        raise ValueError("É obrigatório fornecer um ID de arquivo e/ou um ID de turma e/ou um ID de matéria.")
    
    vinculos = ArquivoTurmaMateria.query
    
    if arquivo_id is not None:
        vinculos = vinculos.filter_by(arquivo_id=arquivo_id)
    
    if turma_id is not None:
        vinculos = vinculos.filter_by(turma_id=turma_id)
    
    if materia_id is not None:
        vinculos = vinculos.filter_by(materia_id=materia_id)
    
    return [vinculo.to_dict() for vinculo in vinculos.all()] if vinculos else None

def criar_vinculo_arquivo_turma_materia(arquivo_id: uuid.UUID, turma_id: uuid.UUID, materia_id: uuid.UUID) -> ArquivoTurmaMateria | None:
    """
    Cria um novo vínculo entre um arquivo, uma turma e uma matéria.

    Espera receber todos esses três parâmetros:
    - `arquivo_id`: uuid.UUID - o ID do arquivo
    - `turma_id`: uuid.UUID - o ID da turma
    - `materia_id`: uuid.UUID - o ID da matéria

    Retorna o vínculo criado se ele for criado com sucesso, e None se o vínculo já existir.
    """
    existe = buscar_vinculos_arquivo_turma_materia(arquivo_id, turma_id, materia_id)
    if existe:
        return None
    
    novo_vinculo = ArquivoTurmaMateria(arquivo_id=arquivo_id, turma_id=turma_id, materia_id=materia_id)
    db.session.add(novo_vinculo)
    db.session.commit()
    return novo_vinculo
