from flask_socketio import SocketIO
from .handlers import handle_connect, handle_mensagem_inicial, handle_nova_mensagem

socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")

@socketio.on("connect")
def on_connect():
    handle_connect()

@socketio.on('mensagem_inicial')
def on_mensagem_inicial():
    handle_mensagem_inicial()

@socketio.on('nova_mensagem')
def on_nova_mensagem():
    handle_nova_mensagem()
