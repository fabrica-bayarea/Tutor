import uuid
from application.models.model_turma import Turma, StatusTurmaEnum
from application.models.model_turma_materia import TurmaMateria
from application.models.model_aluno_turma import AlunoTurma
from application.config.database import db

def buscar_turma_por_id(turma_id: uuid.UUID = None) -> dict | None:
    """
    Busca uma turma no banco de dados usando seu ID.

    Espera receber:
    - `turma_id`: uuid.UUID - o ID da turma
    
    Retorna a turma se ela existir, e None caso contrário.
    """
    turma = Turma.query.filter_by(id=turma_id).first()
    return turma.to_dict() if turma else None

def buscar_id_turma_por_codigo(codigo_turma: str) -> uuid.UUID | None:
    """
    Busca uma turma no banco de dados usando o código fornecido.

    Espera receber:
    - `codigo_turma`: str - o código da turma
    
    Retorna o UUID da turma se ela existir, e None caso contrário.
    """
    turma = Turma.query.filter_by(codigo=codigo_turma).first()
    return turma.id if turma else None

def buscar_codigo_turma_por_id(id_turma: uuid.UUID) -> str | None:
    """
    Busca uma turma no banco de dados usando o ID fornecido.

    Espera receber:
    - `id_turma`: uuid.UUID - o ID da turma
    
    Retorna o código da turma se ela existir, e None caso contrário.
    """
    turma = Turma.query.filter_by(id=id_turma).first()
    return turma.codigo if turma else None


def getAllTurmas(codigo: str, semestre: str, turno: str, status: str):

    query = Turma.query


    if codigo:
        query = query.filter(Turma.codigo.ilike(f"%{codigo}%"))
    
    if semestre:
        query = query.filter(Turma.semestre.ilike(f"%{semestre}%"))
    
    if turno:
        query = query.filter(Turma.turno.ilike(f"%{turno}%"))
    
    if status:
        query = query.filter(Turma.status.ilike(f"%{status}%"))
    
    return query.order_by(Turma.codigo.asc())


def createTurma(codigo: str, semestre: str, turno: str):

    turma = Turma(
        codigo=codigo,
        semestre=semestre,
        turno=turno,
        status=StatusTurmaEnum.ATIVO
    )

    db.session.add(turma)

    db.session.flush()

    db.session.commit()
    return turma.to_dict()


def updateTurma(id: uuid.uuid4, codigo_novo: str, semestre_novo: str, turno_novo: str, status_novo: str):

    turma = Turma.query.get(id)

    if not Turma:
        return None
    
    turma.codigo = codigo_novo
    turma.semestre = semestre_novo
    turma.turno = turno_novo
    turma.status = status_novo

    db.session.commit()

    return turma.to_dict()


def deleteTurma(id: uuid.uuid4):


    turma = Turma.query.get(id)

    if not turma:
        return None, {'turma_nao_encontrada'}
    
    turma_vinculada_materia = db.session.query(TurmaMateria).filter_by(turma_id=id).first()

    if turma_vinculada_materia:
        return None, {'turma_vinculada_a_uma_materia'}
    
    turma_vinculada_aluno = db.session.query(AlunoTurma).filter_by(turma_id=id).first()

    if turma_vinculada_aluno:
        return None, {'turma_vinculada_a_um_aluno'}


    turma.status = StatusTurmaEnum.INATIVO
    db.session.commit()

    return turma, None