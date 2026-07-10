from gevent import monkey
monkey.patch_all()

from flask import Flask, g
from flask_migrate import Migrate
from flask_cors import CORS

from application.config.config import Config
from application.config.database import init_db, db
from application.auth.jwt_handler import definir_cookie_sessao
from application.socket.socket_instance import socketio
from application.routes.route_auth import auth_bp

import application.socket.event_handler

from application.routes import (
    arquivos_bp,
    usuarios_bp,
    turmas_bp,
    materias_bp,
    chats_bp,
    mensagens_bp,
    vinculos_bp,
    data_bp,
    admin_bp,
    llm_bp
)

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

socketio.init_app(app)

CORS(app, 
     resources={r"/(?!socket\.io).*": {"origins": ["https://bayarea.dataiesb.com", "http://localhost:3000"]}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])

@app.after_request
def add_security_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


@app.after_request
def renovar_sessao(response):
    """
    Renova o cookie de sessão (sliding expiration) sempre que uma requisição
    autenticada definir `g.refresh_token` no `token_obrigatorio`. Rotas como o
    logout limpam `g.refresh_token` para não reabrir a sessão.
    """
    novo_token = getattr(g, "refresh_token", None)
    if novo_token:
        definir_cookie_sessao(response, novo_token)
    return response

init_db(app)
migrate = Migrate(app, db)


app.register_blueprint(arquivos_bp, url_prefix="/arquivos")
app.register_blueprint(usuarios_bp, url_prefix="/alunos")
app.register_blueprint(turmas_bp, url_prefix="/turmas")
app.register_blueprint(materias_bp, url_prefix="/materias")
app.register_blueprint(chats_bp, url_prefix="/chats")
app.register_blueprint(mensagens_bp, url_prefix="/mensagens")
app.register_blueprint(vinculos_bp, url_prefix="/vinculos")
app.register_blueprint(data_bp, url_prefix="/data")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(llm_bp)

from application.startup import sincronizar_modelos_no_boot
sincronizar_modelos_no_boot(app)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)