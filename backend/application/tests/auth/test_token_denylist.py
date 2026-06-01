"""
Testes unitários da denylist de tokens/usuários (logout e desativação).

Cobrem os dois back-ends suportados:
- fallback em memória (sem REDIS_URL), usado em dev/single-worker;
- Redis (mockado), incluindo o fallback automático para memória quando o
  Redis falha em tempo de execução.

Os imports pesados do pacote `application` são stubbados para que o módulo possa
ser testado isoladamente (mesmo padrão de `test_primeiro_acesso`).
"""
import sys
from unittest.mock import MagicMock

# Stub das libs/módulos pesados puxados por application/__init__.py.
sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())
sys.modules.setdefault("application.config.vector_database", MagicMock())

import pytest
import application.auth.token_denylist as td


@pytest.fixture(autouse=True)
def reset_state(monkeypatch):
    """Zera o estado global do módulo entre os testes."""
    monkeypatch.setattr(td, "_redis", None)
    monkeypatch.setattr(td, "_init_done", False)
    monkeypatch.setattr(td, "_memoria", set())
    monkeypatch.setattr(td, "_memoria_usuarios", set())
    yield


# ---------------------------------------------------------------------------
# _get_redis — inicialização preguiçosa
# ---------------------------------------------------------------------------

def test_get_redis_sem_url_retorna_none(monkeypatch):
    monkeypatch.delenv("REDIS_URL", raising=False)
    assert td._get_redis() is None
    assert td._init_done is True


def test_get_redis_com_url_conecta_e_pinga(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379")
    fake_client = MagicMock()
    fake_redis_mod = MagicMock()
    fake_redis_mod.from_url.return_value = fake_client
    monkeypatch.setitem(sys.modules, "redis", fake_redis_mod)

    assert td._get_redis() is fake_client
    fake_client.ping.assert_called_once()


def test_get_redis_falha_na_conexao_cai_para_none(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379")
    fake_redis_mod = MagicMock()
    fake_redis_mod.from_url.side_effect = Exception("connection refused")
    monkeypatch.setitem(sys.modules, "redis", fake_redis_mod)

    assert td._get_redis() is None


def test_get_redis_inicializa_uma_unica_vez(monkeypatch):
    monkeypatch.setattr(td, "_init_done", True)
    monkeypatch.setattr(td, "_redis", "cliente-cacheado")
    assert td._get_redis() == "cliente-cacheado"


# ---------------------------------------------------------------------------
# Fallback em memória (sem Redis)
# ---------------------------------------------------------------------------

def test_token_invalidado_em_memoria(monkeypatch):
    monkeypatch.setattr(td, "_get_redis", lambda: None)
    assert td.token_invalido("tok-1") is False
    td.invalidar_token("tok-1")
    assert td.token_invalido("tok-1") is True


def test_bloqueio_de_usuario_em_memoria(monkeypatch):
    monkeypatch.setattr(td, "_get_redis", lambda: None)
    assert td.usuario_bloqueado("u-1") is False
    td.bloquear_usuario("u-1")
    assert td.usuario_bloqueado("u-1") is True
    td.desbloquear_usuario("u-1")
    assert td.usuario_bloqueado("u-1") is False


def test_bloqueio_normaliza_id_para_string(monkeypatch):
    monkeypatch.setattr(td, "_get_redis", lambda: None)
    td.bloquear_usuario(123)
    assert td.usuario_bloqueado("123") is True


# ---------------------------------------------------------------------------
# Caminho Redis (cliente mockado)
# ---------------------------------------------------------------------------

def test_invalidar_token_usa_redis_setex(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    td.invalidar_token("tok-1")
    client.setex.assert_called_once()
    assert "tok-1" not in td._memoria  # não cai para memória quando Redis ok


def test_token_invalido_consulta_redis(monkeypatch):
    client = MagicMock()
    client.exists.return_value = 1
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    assert td.token_invalido("tok-1") is True


def test_bloquear_usuario_usa_redis(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    td.bloquear_usuario("u-1")
    client.setex.assert_called_once()


def test_desbloquear_usuario_usa_redis_delete(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    td.desbloquear_usuario("u-1")
    client.delete.assert_called_once()


def test_usuario_bloqueado_consulta_redis(monkeypatch):
    client = MagicMock()
    client.exists.return_value = 1
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    assert td.usuario_bloqueado("u-1") is True


# ---------------------------------------------------------------------------
# Redis falha em runtime -> fallback automático para memória
# ---------------------------------------------------------------------------

def test_invalidar_token_redis_erro_cai_para_memoria(monkeypatch):
    client = MagicMock()
    client.setex.side_effect = Exception("redis down")
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    td.invalidar_token("tok-1")
    assert "tok-1" in td._memoria


def test_token_invalido_redis_erro_cai_para_memoria(monkeypatch):
    client = MagicMock()
    client.exists.side_effect = Exception("redis down")
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    td._memoria.add("tok-1")
    assert td.token_invalido("tok-1") is True


def test_bloquear_usuario_redis_erro_cai_para_memoria(monkeypatch):
    client = MagicMock()
    client.setex.side_effect = Exception("redis down")
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    td.bloquear_usuario("u-1")
    assert "u-1" in td._memoria_usuarios


def test_desbloquear_usuario_redis_erro_nao_quebra(monkeypatch):
    client = MagicMock()
    client.delete.side_effect = Exception("redis down")
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    # não deve levantar; o discard em memória só roda quando não há cliente
    td.desbloquear_usuario("u-1")


def test_usuario_bloqueado_redis_erro_cai_para_memoria(monkeypatch):
    client = MagicMock()
    client.exists.side_effect = Exception("redis down")
    monkeypatch.setattr(td, "_get_redis", lambda: client)
    td._memoria_usuarios.add("u-1")
    assert td.usuario_bloqueado("u-1") is True
