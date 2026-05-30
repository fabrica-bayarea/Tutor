"""
Denylist de tokens encerrados (logout).

Usa Redis quando `REDIS_URL` está configurado — o que torna a invalidação
persistente entre reinícios e compartilhada entre workers. Cada entrada recebe
TTL igual ao tempo de sessão, de modo que a chave expira sozinha (a lista não
cresce indefinidamente). Sem `REDIS_URL`, recai para um `set()` em memória
(suficiente para desenvolvimento com 1 worker).
"""
import os
import logging

from .jwt_handler import SESSION_IDLE_MINUTES

logger = logging.getLogger(__name__)

_PREFIXO = "denylist:"
_TTL = SESSION_IDLE_MINUTES * 60

_redis = None
_init_done = False
_memoria = set()


def _get_redis():
    """Inicializa o cliente Redis uma única vez. Retorna None se indisponível."""
    global _redis, _init_done
    if _init_done:
        return _redis

    _init_done = True
    url = os.getenv("REDIS_URL")
    if not url:
        return None

    try:
        import redis
        client = redis.from_url(url, socket_connect_timeout=2, socket_timeout=2)
        client.ping()
        _redis = client
    except Exception as e:
        logger.warning("Redis indisponível (%s). Usando denylist em memória.", e)
        _redis = None

    return _redis


def invalidar_token(token: str) -> None:
    """Marca um token como inválido (logout), com expiração automática."""
    client = _get_redis()
    if client:
        try:
            client.setex(f"{_PREFIXO}{token}", _TTL, "1")
            return
        except Exception as e:
            logger.warning("Falha ao gravar denylist no Redis (%s). Fallback memória.", e)
    _memoria.add(token)


def token_invalido(token: str) -> bool:
    """Indica se o token foi encerrado e não deve mais ser aceito."""
    client = _get_redis()
    if client:
        try:
            return client.exists(f"{_PREFIXO}{token}") == 1
        except Exception as e:
            logger.warning("Falha ao ler denylist no Redis (%s). Fallback memória.", e)
    return token in _memoria
