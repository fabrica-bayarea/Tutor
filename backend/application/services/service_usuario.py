import uuid
from application.models import Usuario, AlunoTurma
from application.config.database import db
import uuid as uuid_lib
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from application.models.model_token_convite import TokenConvite
import re

def criar_usuario(
    matricula: str,
    nome: str,
    email: str,
    via_google: bool = False
) -> tuple[dict, str | None]:
    """
    Cria um novo usuário no banco com senha aleatória hasheada.
    Gera um token de convite vinculado ao usuário se não for via Google.

    Espera receber:
    - `matricula`: str - matrícula do usuário
    - `nome`: str - nome do usuário
    - `email`: str - e-mail do usuário
    - `via_google`: bool - indica se o usuário autenticará via Google (padrão: False)

    Retorna uma tupla com:
    - dicionário com os dados do usuário criado
    - token de convite (str) ou None se via_google=True
    """
    senha_aleatoria = secrets.token_hex(16)
    senha_hash = generate_password_hash(senha_aleatoria)

    usuario = Usuario(
        matricula=matricula,
        nome=nome,
        email=email,
        senha=senha_hash,
        role=RoleEnum.ALUNO,
        status=RoleEnum.ATIVO
    )
    db.session.add(usuario)
    db.session.flush()  # garante o ID antes do commit

    token_str = None
    if not via_google:
        token_str = str(uuid_lib.uuid4())
        token = TokenConvite(
            token=token_str,
            usuario_id=usuario.id,
            used=False
        )
        db.session.add(token)

    db.session.commit()
    return usuario.to_dict(), token_str


def buscar_aluno(
    aluno_id: uuid.UUID = None,
    matricula: str = None,
    nome: str = None,
    email: str = None,
    role: str = None
) -> dict[str, str] | None:
    
    aluno = Usuario(
        matricula=matricula,
        nome=nome,
        email=email,
        senha=senha,
        role=RoleEnum.ALUNO,
        status=RoleEnum.ATIVO
    )
    db.session.add(aluno)
    db.session.commit()
    return aluno.to_dict()

def buscar_aluno(aluno_id: uuid.UUID = None, matricula: str = None, nome: str = None, email: str = None, role: str = None) -> dict[str, str] | None:
    """
    Busca um aluno no banco de dados usando um ou mais filtros.

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

    if aluno and check_password_hash(aluno.senha, senha):
        return aluno.to_dict()

    return None

def desativar_aluno(aluno_id: uuid.UUID ):
    """
    Função responsavel por desativar aluno do banco de dados.
    
    Espera receber:
    - `id: ` uuid.UUID - id do aluno que sera desativado

    Retorna uma mensagem mostrando se o aluno foi alterado ou erro se caso não encontrado
    """

    aluno = Usuario.query.get(aluno_id)

    if not aluno:
        return None
    
    aluno.status = RoleEnum.INATIVO.name
    db.session.commit()

    return aluno

def alterar_aluno_por_id(id: uuid.UUID, matricula_nova: str, nome_novo: str, email_novo:str, status_novo: str,  role_nova: str):
    """
    Função atômica, responsável por alterar um usuario no PostgreSQL.

    Espera receber:
    - `nome`: str - o nome novo do aluno
    - `matricula`: str - o número de matrícula do aluno
    - `role`: str - role novo do usuario
    - `email`: str - email novo do aluno
    - `status`: str - status novo do aluno

    Retorna um dicionário com os dados do usuario alterado.
    """
    aluno = Usuario.query.filter_by(id=id).first()
    
    if not aluno:
        return None  # Se não encontrar, retorna None
    

    aluno.matricula = matricula_nova
    aluno.role = role_nova
    aluno.nome = nome_novo
    aluno.email = email_novo
    aluno.status = status_novo

    
    db.session.commit()
    
    return aluno.to_dict()

def reativar_aluno(id: uuid.UUID, status_novo: str):
    """
    Função atômica, responsável por reativar um usuario no PostgreSQL.

    Espera receber:
    - `id: ` uuid.UUID - id do aluno que sera ativado
    - `status`: str - status novo do aluno

    Retorna um dicionário informando que o usuario foi alterado.
    """
    aluno = Usuario.query.filter_by(id=id).first()

    if not aluno:
        return None  # Se não encontrar, retorna None
    
    aluno.status = status_novo

    db.session.commit()

    return aluno.to_dict()


def buscar_alunos_por_filtro(nome: str, matricula: str, turma: str, role: str, status: str):
    """
    Função atômica, responsável por buscar os usuarios no PostgreSQL dada ou não um determinado parametro.

    Espera receber:
    - `nome`: str - o nome  do aluno
    - `matricula`: str - o número de matrícula do aluno
    - `role`: str - role  do usuario
    - `email`: str - email  do aluno
    - `status`: str - status  do aluno

    Retorna uma lista de alunos encontrados
    """
    query = Usuario.query

    if turma:
        query = query.join(AlunoTurma)

    if nome:
        query = query.filter(Usuario.nome.ilike(f"%{nome}%"))

    if matricula:
        query = query.filter(Usuario.matricula.ilike(f"%{matricula}%"))

    if turma:
        query = query.filter(AlunoTurma.turma.ilike(f"%{turma}%"))

    if role:
        query = query.filter(Usuario.role == role)

    if status:
        query = query.filter(Usuario.status == status)

    
    return query.order_by(Usuario.nome.asc())

def validar_token_convite(token: str) -> tuple[dict | None, str]:
    """
    Valida um token de convite de primeiro acesso.

    Espera receber:
    - `token`: str - token UUID a ser validado

    Retorna uma tupla com:
    - dicionário com dados básicos do usuário se o token for válido, None caso contrário
    - status: 'valido' | 'utilizado_ou_inexistente'
    """
    registro = TokenConvite.query.filter_by(token=token).first()

    if not registro or registro.used:
        return None, 'utilizado_ou_inexistente'

    usuario = registro.usuario
    return {'nome': usuario.nome, 'email': usuario.email}, 'valido'

def _validar_forca_senha(senha: str) -> str | None:
    """
    Valida os critérios mínimos de força da senha.

    Espera receber:
    - `senha`: str - senha a ser validada

    Retorna uma mensagem de erro explicativa se a senha for fraca, None se aprovada.
    """
    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres."
    if not re.search(r'[A-Z]', senha):
        return "A senha deve conter ao menos uma letra maiúscula."
    if not re.search(r'[a-z]', senha):
        return "A senha deve conter ao menos uma letra minúscula."
    if not re.search(r'[0-9]', senha):
        return "A senha deve conter ao menos um número."
    return None