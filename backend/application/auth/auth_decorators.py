from functools import wraps
from flask import request, jsonify, g
from .jwt_handler import validar_token

def token_obrigatorio(f):
    """
    Decorador personalizado que verifica se um token JWT válido foi enviado numa requisição.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token ausente"}), 401
        
        payload = validar_token(token)
        if not payload:
            return jsonify({"error": "Token inválido ou expirado"}), 401
        
        g.usuario_id = payload.get("user_id")
        g.usuario_role = payload.get("role")
        return f(*args, **kwargs)
    return wrapper

def apenas_professores(f):
    """
    Decorador personalizado que restringe o acesso da rota apenas para usuários com papel de professor.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(g, "usuario_role") or g.usuario_role != "professor":
            return jsonify({"error": "Acesso negado"}), 403
        return f(*args, **kwargs)
    return wrapper

def apenas_alunos(f):
    """
    Decorador personalizado que restringe o acesso da rota apenas para usuários com papel de aluno.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(g, "usuario_role") or g.usuario_role != "aluno":
            return jsonify({"error": "Acesso negado"}), 403
        return f(*args, **kwargs)
    return wrapper
