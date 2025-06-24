from flask_socketio import SocketIO
from .handlers import *

socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")

@socketio.on("connect")
def on_connect():
    handle_connect()
