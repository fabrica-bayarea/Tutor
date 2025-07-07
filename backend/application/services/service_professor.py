import uuid
from application.models import Professor
from application.config.database import db

def criar_professor(matricula: str, nome: str, email: str, senha: str, cpf: str, data_nascimento: str) -> dict[str, str] | None:
    """
    Função atômica, responsável por criar um professor no PostgreSQL.

    Espera receber:
    - `matricula`: str - o número de matrícula do professor
    - `nome`: str - o nome do professor
    - `email`: str - o email do professor
    - `senha`: str - a senha do professor
    - `cpf`: str - o cpf do professor
    - `data_nascimento`: str - a data de nascimento do professor

    Retorna o professor criado.
    """
    professor = Professor(
        matricula=matricula,
        nome=nome,
        email=email,
        senha=senha,
        cpf=cpf,
        data_nascimento=data_nascimento
    )
    db.session.add(professor)
    db.session.commit()
    return professor.to_dict()

def buscar_professor(professor_id: uuid.UUID = None, matricula: str = None, nome: str = None, email: str = None, cpf: str = None, data_nascimento: str = None) -> dict[str, str] | None:
    """
    Busca um professor no banco de dados usando um ou mais filtros.

    Espera receber um ou mais dos seguintes parâmetros:
    - `professor_id`: uuid.UUID - o ID do professor
    - `matricula`: str - o número de matrícula do professor
    - `nome`: str - o nome do professor
    - `email`: str - o email do professor
    - `cpf`: str - o cpf do professor
    - `data_nascimento`: str - a data de nascimento do professor

    Retorna o professor se ele existir, e None caso contrário.
    """
    if professor_id is not None:
        professor = Professor.query.filter_by(id=professor_id).first()
    
    if matricula is not None:
        professor = Professor.query.filter_by(matricula=matricula).first()
    
    if nome is not None:
        professor = Professor.query.filter_by(nome=nome).first()
    
    if email is not None:
        professor = Professor.query.filter_by(email=email).first()
    
    if cpf is not None:
        professor = Professor.query.filter_by(cpf=cpf).first()
    
    if data_nascimento is not None:
        professor = Professor.query.filter_by(data_nascimento=data_nascimento).first()
    
    return professor.to_dict() if professor else None

def logar_professor(matricula: str, senha: str) -> dict[str, str] | None:
    """
    Função atômica, responsável por logar um professor no PostgreSQL.

    Espera receber:
    - `matricula`: str - o número de matrícula do professor
    - `senha`: str - a senha do professor

    1. Busca um professor no banco de dados usando o número de matrícula fornecido
    2. Verifica se o professor existe e se a senha fornecida é igual à senha do professor
    
    Retorna os dados do professor se o login for válido, e None caso contrário.
    """
    professor = Professor.query.filter_by(matricula=matricula).first()
    
    if professor and professor.senha == senha:
        return professor.to_dict()
    
    return None
