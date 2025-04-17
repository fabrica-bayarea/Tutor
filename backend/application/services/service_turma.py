import uuid
from application.models import Turma

def buscar_id_turma_por_codigo(codigo_turma: str) -> uuid.UUID | None:
    """
    Busca uma turma no banco de dados usando o código fornecido.

    Espera receber:
    - `codigo_turma`: str - o código da turma
    
    Retorna o UUID da turma se ela existir, e None caso contrário.
    """
    turma = Turma.query.filter_by(codigo=codigo_turma).first()
    return turma.id if turma else None
