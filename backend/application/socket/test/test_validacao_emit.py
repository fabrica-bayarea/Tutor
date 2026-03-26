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

from application.socket.Impl.event_handlers import validacao_emit

json_emit_valido = {
    "id_usuario": "550e8400-e29b-41d4-a716-446655440000",
    "id_materia": "550e8400-e29b-41d4-a716-446655440000",
    "LLM": "gpt-4",
    "mensagem": "Olá mundo",
    "chat_novo": True,
    "id_chat": "123e4567-e89b-12d3-a456-426614174000",
    "data_envio": datetime.now()
}

resultado = validacao_emit(json_emit_valido)

print(resultado)

json_emit_invalido = {
    "id_usuario": "teste",
    "id_materia": "teste",
    "LLM": 111,
    "mensagem": " ",
    "chat_novo": "true",
    "id_chat": "teste",
    "data_envio": "111"
}

resultado = validacao_emit(json_emit_invalido)

print(resultado)