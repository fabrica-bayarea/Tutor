import uuid
from application.models import Professor

def buscar_id_professor_por_matricula(matricula: str) -> uuid.UUID | None:
    """
    Busca um professor no banco de dados usando a matrícula fornecida.

    Espera receber:
    - `matricula`: str - o número de matrícula do professor
    
    Retorna o UUID do professor se ele existir, e None caso contrário.
    """
    professor = Professor.query.filter_by(matricula=matricula).first()
    return professor.id if professor else None
