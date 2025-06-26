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

def logar_professor(matricula: str, senha: str) -> dict[str, str] | None:
    """
    Função atômica, responsável por logar um professor no PostgreSQL.

    Espera receber:
    - `matricula`: str - o número de matrícula do professor
    - `senha`: str - a senha do professor

    Retorna os dados do professor se o login for válido, e None caso contrário.
    """
    professor = Professor.query.filter_by(matricula=matricula, senha=senha).first()
    return professor.to_dict() if professor else None
