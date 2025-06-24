from flask_socketio import emit
from application.constants import LLM_UUID
from application.mistral.core import pipeline

def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})
