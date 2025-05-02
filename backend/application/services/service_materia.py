import uuid
from application.models import Materia

def buscar_id_materia_por_codigo(codigo_materia: str) -> uuid.UUID | None:
    """
    Busca uma matéria no banco de dados usando o código fornecido.

    Espera receber:
    - `codigo_materia`: str - o código da matéria
    
    Retorna o UUID da matéria se ela existir, e None caso contrário.
    """
    materia = Materia.query.filter_by(codigo=codigo_materia).first()
    return materia.id if materia else None

def buscar_codigo_materia_por_id(id_materia: uuid.UUID) -> str | None:
    """
    Busca uma matéria no banco de dados usando o ID fornecido.

    Espera receber:
    - `id_materia`: uuid.UUID - o ID da matéria
    
    Retorna o código da matéria se ela existir, e None caso contrário.
    """
    materia = Materia.query.filter_by(id=id_materia).first()
    return materia.codigo if materia else None
