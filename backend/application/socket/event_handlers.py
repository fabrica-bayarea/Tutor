from datetime import datetime
from flask import request
from flask_socketio import SocketIO, emit
from application.config.vector_database import collection
from application.services.service_chat import criar_chat
from application.services.service_mensagem import criar_mensagem, buscar_ultimas_n_mensagens
from application.constants import LLM_UUID
import uuid
import ollama
from application.models.model_chat import Chat
from application.config.database import db
from application.models.model_mensagem import Mensagem
from application.socket.Impl.registrar_chat import registrar_chat
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.socket.Impl.validacao_emit import validacao_emit

socketio = SocketIO(cors_allowed_origins="*", async_mode="gevent")

@socketio.on("connect")
def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})
