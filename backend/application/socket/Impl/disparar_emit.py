from datetime import datetime
from flask_socketio import SocketIO
import traceback
import uuid

def disparar_emit(socketio: SocketIO, evento: str, payload: dict, room: str | None = None):
    try:
        if not isinstance(payload, dict):
            print(f"[Socket Error] payload não é um dicionario")
            return
        
        def preparar_dados(obj):
            if isinstance(obj, dict):
                return {k: preparar_dados(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [preparar_dados(i) for i in obj]
            elif isinstance(obj, uuid.UUID):
                return str(obj)
            return obj
            
        dados_limpos = preparar_dados(payload)
        payload_seguro = { **dados_limpos, "timestamp": datetime.now().isoformat() }
        
        if room: 
            socketio.emit(evento, payload_seguro, room=room)
        else:
            socketio.emit(evento, payload_seguro)

        print(f"[Socket Emit] evento: {evento} | room: {room}")
    except Exception as e:
        traceback.print_exc()
        print(f"[Socket Error] falha ao emitir '{evento}': {str(e)}")
