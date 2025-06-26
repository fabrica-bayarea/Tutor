import jwt
import datetime
from flask import current_app

def gerar_token(user_id: str, role: str, expiracao_min=60) -> str:
    """
    Gera um JWT contendo o ID do usuário e seu papel ('professor' ou 'aluno').

    Espera receber:
        - `user_id`: str - o ID do usuário
        - `role`: str - o papel do usuário ('professor' ou 'aluno')
        - `expiracao_min`: int - a expiração do token em minutos (por padrão, 60 minutos)
    
    Retorna o token JWT gerado.
    """
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=expiracao_min)
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token

def validar_token(token: str) -> dict | None:
    """
    Valida o token JWT e retorna o payload decodificado.

    Espera receber:
        - `token`: str - o token JWT a ser validado
    
    Retorna o payload decodificado do token JWT, ou None se o token for inválido.
    """
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
