from datetime import datetime
import uuid


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
            datetime.fromisoformat(value.replace("Z", "+00:00"))
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
    if "id_materia" not in json_emit or not _is_valid_uuid_(json_emit["id_materia"]):
        erros.append(f"id_materia: '{json_emit.get('id_materia')}'. deve ser um UUID válido.")
    
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

def disparar_emit(socketio: SocketIO, evento: str, payload: dict, room: str | None = None):
    try:
        if not isinstance(payload, dict):
            print(f"[Socket Error] payload não é um dicionario")
            return
        
        payload_seguro = { **payload, "timestamp": datetime.now().isoformat() }
        
        if room: 
            socketio.emit(evento, payload_seguro, room=room)
        else:
            socketio.emit(evento, payload_seguro)

        print(f"[Socket Emit] evento: {evento} | room: {room}")
    except Exception as e:
       print(f"[Socket Error] falha ao emitir '{evento}': {str(e)}")