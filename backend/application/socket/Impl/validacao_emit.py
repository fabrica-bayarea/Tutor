from datetime import datetime
import uuid
from typing import Any

def _is_valid_uuid_(value: Any): 
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError):
        return False
    

def _is_valid_iso_date_(value: Any): 
    if isinstance(value, datetime): 
        return True
    
    if isinstance(value, str):
        try: 
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False
    return False


def validacao_emit(json_emit: dict[str, Any]): 
    erros = []

    if "id_usuario" not in json_emit or not _is_valid_uuid_(json_emit["id_usuario"]): 
        erros.append("id_usuario inválido.")
    
    if "materia_id" not in json_emit or not _is_valid_uuid_(json_emit["materia_id"]):
        erros.append("id_materia inválido.")
    
    if "mensagem" not in json_emit or not isinstance(json_emit["mensagem"], str) or not json_emit["mensagem"].strip():
        erros.append("mensagem inválida.")

    if "historico" not in json_emit or not isinstance(json_emit["historico"], list):
        erros.append("historico deve ser uma lista.")

    if "chat_novo" not in json_emit or not isinstance(json_emit["chat_novo"], bool):
        erros.append("chat_novo deve ser boolean.")

    if not json_emit.get("chat_novo"):
        if "id_chat" not in json_emit or not _is_valid_uuid_(json_emit["id_chat"]):
            erros.append("id_chat inválido.")

    if "data_envio" not in json_emit or not _is_valid_iso_date_(json_emit["data_envio"]):
        erros.append("data_envio inválido.")

    if erros:
        raise ValueError(erros)
