from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from application.config.config import Config
from application.config.database import init_db, db

from application.routes import (
    arquivos_bp,
    usuarios_bp,
    turmas_bp,
    materias_bp,
    chats_bp,
    mensagens_bp,
    vinculos_bp
)

import application.models

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

CORS(
    app,
    origins=["http://localhost:3000"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

@app.after_request
def add_security_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

init_db(app)
migrate = Migrate(app, db)


app.register_blueprint(arquivos_bp, url_prefix="/arquivos")
app.register_blueprint(usuarios_bp, url_prefix="/usuario")
app.register_blueprint(turmas_bp, url_prefix="/turmas")
app.register_blueprint(materias_bp, url_prefix="/materias")
app.register_blueprint(chats_bp, url_prefix="/chats")
app.register_blueprint(mensagens_bp, url_prefix="/mensagens")
app.register_blueprint(vinculos_bp, url_prefix="/vinculos")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)