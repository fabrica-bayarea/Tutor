import uuid
from application.models import Aluno
from application.config import db

def criar_aluno(matricula: str, nome: str, email: str, senha: str, cpf: str, data_nascimento: str) -> dict[str, str] | None:
    """
    Função atômica, responsável por criar um aluno no PostgreSQL.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `senha`: str - a senha do aluno
    - `cpf`: str - o cpf do aluno
    - `data_nascimento`: str - a data de nascimento do aluno

    Retorna um dicionário com os dados do aluno criado.
    """
    aluno = Aluno(
        matricula=matricula,
        nome=nome,
        email=email,
        senha=senha,
        cpf=cpf,
        data_nascimento=data_nascimento
    )
    db.session.add(aluno)
    db.session.commit()
    return aluno.to_dict()

def buscar_aluno(aluno_id: uuid.UUID = None, matricula: str = None, nome: str = None, email: str = None, cpf: str = None, data_nascimento: str = None) -> dict[str, str] | None:
    """
    Busca um aluno no banco de dados usando um ou mais filtros.

    Espera receber um ou mais dos seguintes parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `cpf`: str - o cpf do aluno
    - `data_nascimento`: str - a data de nascimento do aluno

    Retorna um dicionário com os dados do aluno se ele existir, e None caso contrário.
    """
    if aluno_id is not None:
        aluno = Aluno.query.filter_by(aluno_id=aluno_id).first()
    
    if matricula is not None:
        aluno = Aluno.query.filter_by(matricula=matricula).first()
    
    if nome is not None:
        aluno = Aluno.query.filter_by(nome=nome).first()
    
    if email is not None:
        aluno = Aluno.query.filter_by(email=email).first()
    
    if cpf is not None:
        aluno = Aluno.query.filter_by(cpf=cpf).first()
    
    if data_nascimento is not None:
        aluno = Aluno.query.filter_by(data_nascimento=data_nascimento).first()
    
    return aluno.to_dict() if aluno else None

def logar_aluno(matricula: str, senha: str) -> dict[str, str] | None:
    """
    Função atômica, responsável por logar um aluno no PostgreSQL.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `senha`: str - a senha do aluno

    1. Busca um aluno no banco de dados usando o número de matrícula fornecido
    2. Verifica se o aluno existe e se a senha fornecida é igual à senha do aluno
    
    Retorna um dicionário com os dados do aluno se o login for válido, e None caso contrário.
    """
    aluno = Aluno.query.filter_by(matricula=matricula).first()
    
    if aluno and aluno.senha == senha:
        return aluno.to_dict()
    
    return None
