from functools import wraps
from flask import request, jsonify, g
from .jwt_handler import validar_token, gerar_token
# Denylist persistente (Redis com fallback em memória) — ver token_denylist.py.
from .token_denylist import token_invalido, usuario_bloqueado


def extrair_token():

    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]

    token_cookie = request.cookies.get("token")

    if token_cookie:
        return token_cookie

    return None


def token_obrigatorio(f):
    """
    Decorador personalizado que verifica se um token JWT válido foi enviado numa requisição.

    Em caso de sucesso, agenda a renovação da sessão (sliding expiration): grava
    em `g.refresh_token` um token novo com a janela de inatividade reiniciada,
    que o `after_request` reescreve no cookie. Assim, cada requisição autenticada
    estende a sessão; após o período de inatividade configurado, o token expira
    e a próxima requisição recebe 401.
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

        # GAP-02-B: usuário desativado tem a sessão encerrada na próxima requisição.
        if usuario_bloqueado(g.usuario_id):
            return jsonify({"error": "Sessão encerrada. Conta desativada."}), 401

        g.refresh_token = gerar_token(g.usuario_id, g.usuario_role)
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

    O claim `role` do JWT guarda o nome do papel (RoleEnum.name), por isso a
    comparação é com 'PROFESSOR' — alinhada a `apenas_admins` (GAP-01-A).
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(g, "usuario_role") or g.usuario_role != "PROFESSOR":
            return jsonify({"error": "Acesso negado"}), 403
        return f(*args, **kwargs)
    return wrapper

def apenas_alunos(f):
    """
    Decorador personalizado que restringe o acesso da rota apenas para usuários com papel de aluno.

    Compara contra o nome do papel ('ALUNO'), como gravado no claim `role` do
    JWT (GAP-01-A).
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(g, "usuario_role") or g.usuario_role != "ALUNO":
            return jsonify({"error": "Acesso negado"}), 403
        return f(*args, **kwargs)
    return wrapper
