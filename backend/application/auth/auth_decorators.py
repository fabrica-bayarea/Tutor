from functools import wraps
from flask import request, jsonify, g
from .jwt_handler import validar_token
from application.models.model_usuario import  RoleEnum


TOKENS_INVALIDADOS = set()

def extrair_token():

    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]

    token_cookie = request.cookies.get("token")

    if token_cookie:
        return token_cookie

    return None


def invalidar_token(token):
    TOKENS_INVALIDADOS.add(token)


def token_invalido(token):
    return token in TOKENS_INVALIDADOS


def token_obrigatorio(f):
    """
    Decorador personalizado que verifica se um token JWT válido foi enviado numa requisição.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = extrair_token()
        if not token:
            return jsonify({"error": "Token ausente"}), 401
        
        if token_invalido(token):
            return jsonify({"Error": "Token invalido"}), 401
        
        payload = validar_token(token)
        if not payload:
            return jsonify({"error": "Token inválido ou expirado"}), 401
        
        g.usuario_id = payload.get("user_id")
        g.usuario_role = payload.get("role")
        return f(*args, **kwargs)
    return wrapper

def apenas_admins(f):
    """
    Decorador personalizado que restringe o acesso da rota apenas para usuários com papel de admin.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):

        if (
            not hasattr(g, "usuario_role") or
            g.usuario_role != "ADMIN"
        ):
            return jsonify({"error": "Acesso negado"}), 403

        return f(*args, **kwargs)

    return wrapper

def apenas_professores(f):
    """
    Decorador personalizado que restringe o acesso da rota apenas para usuários com papel de professor.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(g, "usuario_role") or g.usuario_role not in ['1', '2']:
            return jsonify({"error": "Acesso negado"}), 403
        return f(*args, **kwargs)
    return wrapper

def apenas_alunos(f):
    """
    Decorador personalizado que restringe o acesso da rota apenas para usuários com papel de aluno.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(g, "usuario_role") or g.usuario_role != "3":
            return jsonify({"error": "Acesso negado"}), 403
        return f(*args, **kwargs)
    return wrapper
