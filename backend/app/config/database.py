from flask_sqlalchemy import SQLAlchemy
from config.config import Config

db = SQLAlchemy() # Cria a instância do SQLAlchemy

def init_db(app):
    """Configura e inicializa o banco de dados com a aplicação Flask."""
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
