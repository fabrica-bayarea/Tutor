from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from application.config.config import Config
from application.config.database import init_db, db
from application.routes import arquivos_bp, professores_bp, alunos_bp, turmas_bp, materias_bp, chats_bp, mensagens_bp, vinculos_bp
from application.socket import socketio

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Adiciona cabeçalhos de segurança
@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    if 'X-Powered-By' in response.headers:
        del response.headers['X-Powered-By']
    return response

init_db(app)
migrate = Migrate(app, db)

app.register_blueprint(arquivos_bp, url_prefix="/arquivos")
app.register_blueprint(professores_bp, url_prefix="/professores")
app.register_blueprint(alunos_bp, url_prefix="/alunos")
app.register_blueprint(turmas_bp, url_prefix="/turmas")
app.register_blueprint(materias_bp, url_prefix="/materias")
app.register_blueprint(chats_bp, url_prefix="/chats")
app.register_blueprint(mensagens_bp, url_prefix="/mensagens")
app.register_blueprint(vinculos_bp, url_prefix="/vinculos")

if __name__ == "__main__":
    socketio.init_app(app)
    socketio.run(app, debug=True)
