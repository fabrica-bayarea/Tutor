import uuid
from application.models import Usuario
from application.config.database import db

def criar_aluno(matricula: str, nome: str, email: str, senha: str, data_nascimento: str) -> dict[str, str] | None:
    """
    Função atômica, responsável por criar um aluno no PostgreSQL.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `senha`: str - a senha do aluno

    Retorna um dicionário com os dados do aluno criado.
    """
    aluno = Aluno(
        matricula=matricula,
        nome=nome,
        email=email,
        senha=senha,
        role=3
    )
    db.session.add(aluno)
    db.session.commit()
    return aluno.to_dict()

def buscar_aluno(aluno_id: uuid.UUID = None, matricula: str = None, nome: str = None, email: str = None, role: str = None) -> dict[str, str] | None:
    """
    Busca um aluno no banco de dados usando um ou mais filtros.

    Espera receber um ou mais dos seguintes parâmetros:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `matricula`: str - o número de matrícula do aluno
    - `nome`: str - o nome do aluno
    - `email`: str - o email do aluno
    - `role`: str - a função do usuario

    Retorna um dicionário com os dados do aluno se ele existir, e None caso contrário.
    """
    # Se um ID específico for passado, a busca é direta e ignora os outros campos.
    if aluno_id:
        aluno = Aluno.query.filter_by(id=aluno_id).first()
        return aluno.to_dict() if aluno else None
    
    # Cria uma lista de filtros baseada nos parâmetros que não são None
    filtros = []

    if matricula:
        filtros.append(Aluno.matricula == matricula)

    if email:
        filtros.append(Aluno.email == email)

    if nome:
        filtros.append(Aluno.nome == nome)
    
    if role:
        filtros.append(Aluno.role == role)
        
    aluno = None

    if filtros:
        aluno = Aluno.query.filter(db.or_(*filtros)).first()
    
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

def alterar_aluno(matricula: str, role: str):
    """
    Função atômica, responsável por alterar a role de um usuario no PostgreSQL.

    Espera receber:
    - `matricula`: str - o número de matrícula do aluno
    - `role`: str - role do usuario

    Retorna um dicionário com os dados do usuario alterado.
    """
    aluno = Aluno.query.filter_by(matricula=matricula).first()
    
    if not aluno:
        return None  # Se não encontrar, retorna None
    
    aluno.role = role
    
    db.session.commit()
    
    return aluno.to_dict()

