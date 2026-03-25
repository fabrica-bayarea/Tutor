import datetime
from flask import request
from flask_socketio import SocketIO, emit
from application.config.vector_database import collection
from application.services.service_chat import criar_chat
from application.services.service_mensagem import criar_mensagem, buscar_ultimas_n_mensagens
from application.constants import LLM_UUID
import uuid
import ollama

socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")

@socketio.on("connect")
def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})

def _is_valid_uuid_(value: any): 
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError):
        return False
    

def _is_valid_iso_date_(value: any): 
    if isinstance(value, datetime): 
        return True
    
    if isinstance(value, str):
        try: 
            datetime.fromisoformart(value.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False
    return False


def validacao_emit(json_emit: dict[str, any]): 
    erros = []

    # id_usuario
    if "id_usuario" not in json_emit or not _is_valid_uuid_(json_emit["id_usuario"]): 
        erros.append(f"id_usuario: '{json_emit.get('id_usuario')}'. deve ser um UUID válido.")
    
    # id_materia
    if "id_materia" not in json_emit or not isinstance(json_emit["id_materia"], str) or not json_emit["id_materia"].strip():
        erros.append(f"id_materia inválido: '{json_emit.get('id_materia')}'. Deve ser uma string.")
    
    #LLM
    if "LLM" not in json_emit or not isinstance(json_emit["LLM"], str) or not json_emit["LLM"].strip():
        erros.append(f"LLM deve ser uma String: '{json_emit.get('LLM')}'.")
    
    #mensagem
    if "mensagem" not in json_emit or not isinstance(json_emit["mensagem"], str) or not json_emit["mensagem"].strip():
        erros.append(f"A menssgem: '{json_emit.get('mensagem')}'. Deve ser uma String e não pode estar vazia ou conter apenas espaços.")

    #chat_novo
    if "chat_novo" not in json_emit or not isinstance(json_emit["chat_novo"], bool):
        erros.append("chat_novo deve ser estritamente um valor Booleano (true/false).")
    
    #id_chat
    if "id_chat" not in json_emit or not _is_valid_uuid_(json_emit["id_chat"]):
        erros.append(f"id_chat: '{json_emit.get('id_usuario')}' deve ser um UUID válido.")
    
    #data_envio
    if "data_envio" not in json_emit or not _is_valid_iso_date_(json_emit["data_envio"]):
        erros.append("data_envio deve validar se o formato corresponde a uma data válida (ISO 8601 ou objeto Date).")
    
    return {
        "Valido": len(erros) == 0,
        "Invalido": erros
    }