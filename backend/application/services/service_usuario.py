import uuid
import re
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

from application.models.model_usuario import Usuario, RoleEnum
from application.models.model_aluno_turma import AlunoTurma
from application.models.model_token_convite import TokenConvite
from application.config.database import db

def criar_usuario(
    matricula: str,
    nome: str,
    email: str,
    via_google: bool = False
) -> tuple[dict, str | None]:
    """
    Cria um novo usuário no banco com senha aleatória.
    Gera um token de convite se não for via Google.
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
    db.session.flush()

    token_str = None
    if not via_google:
        token_str = str(uuid.uuid4())
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
) -> dict | None:
    """
    Busca um aluno no banco usando filtros flexíveis.
    """
    if aluno_id:
        aluno = Usuario.query.get(aluno_id)
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


def logar_aluno(matricula: str, senha: str) -> dict | None:
    """Autentica um usuário com matrícula e senha."""
    aluno = Usuario.query.filter_by(matricula=matricula).first()
    if aluno and check_password_hash(aluno.senha, senha):
        return aluno.to_dict()
    return None


def desativar_aluno(aluno_id: uuid.UUID):
    """Desativa um aluno alterando seu status para INATIVO."""
    aluno = Usuario.query.get(aluno_id)
    if not aluno:
        return None
    
    aluno.status = RoleEnum.INATIVO
    db.session.commit()
    return aluno


def alterar_aluno_por_id(id: uuid.UUID, matricula_nova: str, nome_novo: str, email_novo: str, status_novo: str, role_nova: str):
    """Altera os dados de um usuário existente."""
    aluno = Usuario.query.get(id)
    if not aluno:
        return None 

    aluno.matricula = matricula_nova
    aluno.nome = nome_novo
    aluno.email = email_novo
    aluno.role = role_nova
    aluno.status = status_novo
    
    db.session.commit()
    return aluno.to_dict()


def reativar_aluno(id: uuid.UUID, status_novo: str = RoleEnum.ATIVO):
    """Reativa um usuário no sistema."""
    aluno = Usuario.query.get(id)
    if not aluno:
        return None 
    
    aluno.status = status_novo
    db.session.commit()
    return aluno.to_dict()


def buscar_alunos_por_filtro(nome: str, matricula: str, turma: str, role: str, status: str):
    """Busca avançada de alunos com suporte a joins de turma."""
    query = Usuario.query

    if turma:
        query = query.join(AlunoTurma).filter(AlunoTurma.turma.ilike(f"%{turma}%"))

    if nome:
        query = query.filter(Usuario.nome.ilike(f"%{nome}%"))
    if matricula:
        query = query.filter(Usuario.matricula.ilike(f"%{matricula}%"))
    if role:
        query = query.filter(Usuario.role == role)
    if status:
        query = query.filter(Usuario.status == status)
    
    return query.order_by(Usuario.nome.asc())


def validar_token_convite(token: str) -> tuple[dict | None, str]:
    """Valida se um token de convite existe e ainda não foi usado."""
    registro = TokenConvite.query.filter_by(token=token).first()

    if not registro or registro.used:
        return None, 'utilizado_ou_inexistente'

    usuario = registro.usuario
    return {'nome': usuario.nome, 'email': usuario.email}, 'valido'


def definir_senha_primeiro_acesso(token: str, password: str) -> dict | None:
    """Aplica a nova senha e invalida o token de convite."""
    # Validação de força de senha simplificada aqui ou chamada externa
    erro_senha = _validar_forca_senha(password)
    if erro_senha:
        return None # Ou levantar uma exceção personalizada

    registro = TokenConvite.query.filter_by(token=token).first()
    if not registro or registro.used:
        return None

    usuario = registro.usuario
    usuario.senha = generate_password_hash(password)
    registro.used = True

    db.session.commit()
    return usuario.to_dict()



def _validar_forca_senha(senha: str) -> str | None:
    """Critérios: 8+ chars, Maiúscula, Minúscula e Número."""
    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres."
    if not re.search(r'[A-Z]', senha):
        return "A senha deve conter ao menos uma letra maiúscula."
    if not re.search(r'[a-z]', senha):
        return "A senha deve conter ao menos uma letra minúscula."
    if not re.search(r'[0-9]', senha):
        return "A senha deve conter ao menos um número."
    return None

def buscar_professor() -> dict | None:
    return Usuario.query.filter(Usuario.role == RoleEnum.PROFESSOR)