import os
import jwt
import datetime
from flask import current_app

# Tempo de inatividade (em minutos) após o qual a sessão expira. Configurável
# via .env (US-01-RNF3 / US-05-RN2). A renovação por atividade (sliding) é feita
# em `token_obrigatorio` + `after_request`.
SESSION_IDLE_MINUTES = int(os.getenv("SESSION_IDLE_MINUTES", 60))
# Atributos do cookie de sessão, configuráveis por ambiente.
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")


def gerar_token(user_id: str, role: str, expiracao_min: int | None = None) -> str:
    """
    Gera um JWT contendo o ID do usuário e seu papel ('professor' ou 'aluno').

    Espera receber:
        - `user_id`: str - o ID do usuário
        - `role`: str - o papel do usuário ('professor' ou 'aluno')
        - `expiracao_min`: int | None - expiração do token em minutos. Se None,
          usa `SESSION_IDLE_MINUTES` (valor configurável da plataforma).

    Retorna o token JWT gerado.
    """
    if expiracao_min is None:
        expiracao_min = SESSION_IDLE_MINUTES

    payload = {
        "user_id": str(user_id),
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiracao_min)
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token


def definir_cookie_sessao(response, token: str):
    """
    Escreve o cookie de sessão (httponly) na resposta, com `max_age` alinhado ao
    tempo de inatividade configurado. Fonte única para login, primeiro acesso e
    renovação por atividade.
    """
    response.set_cookie(
        "token",
        token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=SESSION_IDLE_MINUTES * 60,
        path="/",
    )
    return response

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
