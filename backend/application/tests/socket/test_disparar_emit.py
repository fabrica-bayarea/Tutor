from datetime import datetime
import sys
from unittest.mock import MagicMock

#Tive que mockar alguns import para poder rodar a função isoladamente

sys.modules["chromadb"] = MagicMock()
sys.modules["application.config.vector_database"] = MagicMock()
sys.modules["flask_sqlalchemy"] = MagicMock()
sys.modules["application.config.database"] = MagicMock()
sys.modules["application.services.service_chat"] = MagicMock()
sys.modules["application.services.service_mensagem"] = MagicMock()
sys.modules["application.models"] = MagicMock()
sys.modules["sqlalchemy"] = MagicMock()
sys.modules["sqlalchemy.sql"] = MagicMock()
sys.modules["ollama"] = MagicMock()

socketio_mock = MagicMock()

from application.socket.Impl.disparar_emit import disparar_emit

#teste de sucesso

json_emit_sem_room = {
    "mensagem": "sem ids"
}

disparar_emit(socketio_mock, "teste", json_emit_sem_room)

assert socketio_mock.emit.called, "emit não foi chamado no caso sem room"

args, kwargs = socketio_mock.emit.call_args

assert args[0] == "teste"
assert "timestamp" in args[1]
assert "room" not in kwargs

print("Teste sem room passou!")

#teste de bloqueio

socketio_mock.emit.reset_mock()

payload_invalido = "isso não é dict"

disparar_emit(socketio_mock, "teste", payload_invalido)

assert not socketio_mock.emit.called, "emit não deveria ser chamado"

print("Teste de payload inválido passou!")