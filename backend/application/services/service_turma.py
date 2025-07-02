import uuid
from application.models import Turma

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
