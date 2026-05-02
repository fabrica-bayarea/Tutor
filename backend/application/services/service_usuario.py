import uuid
from application.models import Usuario
from application.config.database import db


def buscar_aluno(
    aluno_id: uuid.UUID = None,
    matricula: str = None,
    nome: str = None,
    email: str = None,
    role: str = None
) -> dict[str, str] | None:
    """
    Busca um usuário no banco de dados usando um ou mais filtros.

    Espera receber um ou mais dos seguintes parâmetros:
    - `aluno_id`: uuid.UUID - o ID do usuário
    - `matricula`: str - o número de matrícula
    - `nome`: str - o nome do usuário
    - `email`: str - o email do usuário
    - `role`: str - a role do usuário

    Retorna um dicionário com os dados do usuário se encontrado, None caso contrário.
    """
    if aluno_id:
        aluno = Usuario.query.filter_by(id=aluno_id).first()
        return aluno.to_dict() if aluno else None

    filtros = []

    if matricula:
        filtros.append(Usuario.matricula == matricula)
    if email:
        filtros.append(Usuario.email == email)
    if nome:
        filtros.append(Usuario.nome == nome)
    if role:
        filtros.append(Usuario.role == role)

    if not filtros:
        return None

    aluno = Usuario.query.filter(db.or_(*filtros)).first()
    return aluno.to_dict() if aluno else None


def logar_aluno(matricula: str, senha: str) -> dict[str, str] | None:
    """
    Autentica um usuário com matrícula e senha.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `senha`: str - a senha do aluno

    Retorna um dicionário com os dados do usuário se as credenciais forem válidas,
    None caso contrário.
    """
    aluno = Usuario.query.filter_by(matricula=matricula).first()

    if aluno and aluno.senha == senha:
        return aluno.to_dict()

    return None