import os
from flask_socketio import SocketIO

# Origem específica (não "*") é obrigatória para que o handshake aceite o cookie
# de sessão com credenciais. Configurável via FRONTEND_URL.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

socketio = SocketIO(cors_allowed_origins=[FRONTEND_URL], async_mode="gevent")
