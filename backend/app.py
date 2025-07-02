from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from application.config.config import Config
from application.config.database import init_db, db
from application.config.vector_database import chroma_client
from application.routes import arquivos_bp, links_bp, professores_bp, alunos_bp, turmas_bp, materias_bp, vinculos_bp, rag_bp
from application.socket import socketio

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})
init_db(app)
migrate = Migrate(app, db)

collection = chroma_client.get_or_create_collection(name="documentos")

app.register_blueprint(arquivos_bp, url_prefix="/arquivos")
app.register_blueprint(links_bp, url_prefix="/links")
app.register_blueprint(professores_bp, url_prefix="/professores")
app.register_blueprint(alunos_bp, url_prefix="/alunos")
app.register_blueprint(turmas_bp, url_prefix="/turmas")
app.register_blueprint(materias_bp, url_prefix="/materias")
app.register_blueprint(vinculos_bp, url_prefix="/vinculos")
app.register_blueprint(rag_bp, url_prefix="/rag")

if __name__ == "__main__":
    socketio.init_app(app)
    socketio.run(app, debug=True)
