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
