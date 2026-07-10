from flask_socketio import SocketIO

socketio = SocketIO(
    cors_allowed_origins=["https://bayarea.dataiesb.com", "http://localhost:3000"],
    async_mode="gevent",
)
