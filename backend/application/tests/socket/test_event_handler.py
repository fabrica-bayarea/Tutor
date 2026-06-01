"""
Testes do handshake autenticado do WebSocket (GAP-06-F).

Cobrem a autenticação por cookie no connect, o registro/baixa da identidade por
`sid` e a rejeição de mensagens sem sessão autenticada. Tudo mockado — não há
servidor socket.io real.
"""
import sys
import importlib
from unittest.mock import MagicMock, patch

# Stub das libs externas pesadas (mas NÃO de socket_instance/event_handler, que
# precisam ser reais para os @socketio.on devolverem as funções de verdade).
sys.modules.setdefault("chromadb", MagicMock())
sys.modules.setdefault("ollama", MagicMock())
sys.modules.setdefault("application.config.vector_database", MagicMock())

# Outros testes podem ter stubado estes módulos em sys.modules; garante os reais.
for _m in ("application.socket.event_handler", "application.socket.socket_instance"):
    if isinstance(sys.modules.get(_m), MagicMock):
        del sys.modules[_m]

import application.socket.socket_instance  # noqa: E402  (garante módulo real)
import application.socket.event_handler as eh  # noqa: E402

if isinstance(eh, MagicMock) or not hasattr(eh, "_autenticar_handshake"):
    eh = importlib.reload(importlib.import_module("application.socket.event_handler"))

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _limpa_sessoes():
    eh.SOCKET_USUARIOS.clear()
    yield
    eh.SOCKET_USUARIOS.clear()


# ---------------------------------------------------------------------------
# _autenticar_handshake
# ---------------------------------------------------------------------------

def test_handshake_sem_token_retorna_none():
    with patch.object(eh, "extrair_token", return_value=None):
        assert eh._autenticar_handshake() is None


def test_handshake_token_na_denylist_retorna_none():
    with patch.object(eh, "extrair_token", return_value="tok"), \
         patch.object(eh, "token_invalido", return_value=True):
        assert eh._autenticar_handshake() is None


def test_handshake_payload_invalido_retorna_none():
    with patch.object(eh, "extrair_token", return_value="tok"), \
         patch.object(eh, "token_invalido", return_value=False), \
         patch.object(eh, "validar_token", return_value=None):
        assert eh._autenticar_handshake() is None


def test_handshake_sucesso_retorna_user_id():
    with patch.object(eh, "extrair_token", return_value="tok"), \
         patch.object(eh, "token_invalido", return_value=False), \
         patch.object(eh, "validar_token", return_value={"user_id": "u-42"}):
        assert eh._autenticar_handshake() == "u-42"


# ---------------------------------------------------------------------------
# connect / disconnect
# ---------------------------------------------------------------------------

def test_connect_rejeita_sem_autenticacao():
    with patch.object(eh, "_autenticar_handshake", return_value=None):
        assert eh.handle_connect() is False


def test_connect_registra_identidade_e_confirma():
    fake_req = MagicMock(sid="sid-1")
    with patch.object(eh, "_autenticar_handshake", return_value="u-1"), \
         patch.object(eh, "request", fake_req), \
         patch.object(eh, "emit") as mock_emit:
        eh.handle_connect()
    assert eh.SOCKET_USUARIOS["sid-1"] == "u-1"
    mock_emit.assert_called_once()


def test_disconnect_remove_identidade():
    eh.SOCKET_USUARIOS["sid-1"] = "u-1"
    fake_req = MagicMock(sid="sid-1")
    with patch.object(eh, "request", fake_req):
        eh.handle_disconnect()
    assert "sid-1" not in eh.SOCKET_USUARIOS


# ---------------------------------------------------------------------------
# maestro (mensagem_inicial)
# ---------------------------------------------------------------------------

def test_maestro_sem_sessao_emite_sessao_expirada():
    fake_req = MagicMock(sid="sid-x")
    with patch.object(eh, "request", fake_req), \
         patch.object(eh, "disparar_emit") as mock_disp:
        eh.maestro({"id_usuario": "qualquer"})
    evento = mock_disp.call_args.args[1]
    assert evento == "sessao_expirada"


def test_maestro_autenticado_agenda_processamento_com_identidade_do_servidor():
    eh.SOCKET_USUARIOS["sid-1"] = "u-real"
    fake_req = MagicMock(sid="sid-1")
    fake_socketio = MagicMock()
    fake_app = MagicMock()
    fake_app._get_current_object.return_value = "app-obj"
    with patch.object(eh, "request", fake_req), \
         patch.object(eh, "socketio", fake_socketio), \
         patch.object(eh, "current_app", fake_app):
        # id_usuario do payload deve ser ignorado em favor da identidade do handshake
        eh.maestro({"id_usuario": "id-forjado", "mensagem": "oi"})

    fake_socketio.start_background_task.assert_called_once()
    data_arg = fake_socketio.start_background_task.call_args.args[1]
    assert data_arg["id_usuario"] == "u-real"
