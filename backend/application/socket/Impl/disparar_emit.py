from datetime import datetime
from flask_socketio import SocketIO

async def disparar_emit(socketio: SocketIO, evento: str, payload: dict, room: str | None = None):
    try:
        if not isinstance(payload, dict):
            print(f"[Socket Error] payload não é um dicionario")
            return
        
        payload_seguro = { **payload, "timestamp": datetime.now().isoformat() }
        
        if room: 
            await socketio.emit(evento, payload_seguro, room=room)
        else:
            await socketio.emit(evento, payload_seguro)

        print(f"[Socket Emit] evento: {evento} | room: {room}")
    except Exception as e:
       print(f"[Socket Error] falha ao emitir '{evento}': {str(e)}")
