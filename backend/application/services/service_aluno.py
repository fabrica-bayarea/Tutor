import uuid
from application.models import Aluno
from application.config import db

def criar_aluno(matricula: str, nome: str, email: str, cpf: str, data_nascimento: str) -> dict[str, str] | None:
    """
    Função atômica, responsável por criar um aluno no PostgreSQL.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `cpf`: str - o cpf do aluno
    - `data_nascimento`: str - a data de nascimento do aluno

    Retorna o aluno criado.
    """
    aluno = Aluno(
        matricula=matricula,
        nome=nome,
        email=email,
        cpf=cpf,
        data_nascimento=data_nascimento
    )
    db.session.add(aluno)
    db.session.commit()
    return aluno.to_dict()

def buscar_aluno_por_id(aluno_id: uuid.UUID) -> dict[str, str] | None:
    """
    Busca um aluno no banco de dados usando o ID fornecido.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno

    Retorna o aluno se ele existir, e None caso contrário.
    """
    aluno = Aluno.query.get(aluno_id)
    return aluno.to_dict() if aluno else None
