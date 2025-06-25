from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from application.config import *
from application.libs import *
from application.models import *
from application.routes import *
from application.services import *
from application.socket import socketio

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY
CORS(app, resources={r"/*": {"origins": "*"}})
init_db(app)
migrate = Migrate(app, db)

collection = chroma_client.get_or_create_collection(name="documentos")

app.register_blueprint(arquivos_bp, url_prefix="/arquivos")
app.register_blueprint(links_bp, url_prefix="/links")
app.register_blueprint(professores_bp, url_prefix="/professores")
app.register_blueprint(alunos_bp, url_prefix="/alunos")
app.register_blueprint(alunos_turmas_bp, url_prefix="/alunos_turmas")
app.register_blueprint(rag_bp, url_prefix="/rag")

if __name__ == "__main__":
    socketio.init_app(app)
    socketio.run(app, debug=True)
