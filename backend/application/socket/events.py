from flask_socketio import SocketIO
from .handlers import *

socketio = SocketIO(cors_allowed_origins="*")
