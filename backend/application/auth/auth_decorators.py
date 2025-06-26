from functools import wraps
from flask import request, jsonify, g
from .jwt_handler import validar_token

def token_obrigatorio(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token ausente"}), 401
        
        payload = validar_token(token)
        if not payload:
            return jsonify({"error": "Token inválido ou expirado"}), 401
        
        g.usuario_id = payload.get("user_id")
        return f(*args, **kwargs)
    return wrapper
