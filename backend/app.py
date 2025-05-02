from flask import Flask
from flask_migrate import Migrate
from application.config import *
from application.libs import *
from application.models import *
from application.routes import *
from application.services import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/links/*": {"origins": "*"},
    r"/arquivos/*": {"origins": "*"}
})
init_db(app)
migrate = Migrate(app, db)

collection = chroma_client.get_or_create_collection(name="documentos")

app.register_blueprint(arquivos_bp, url_prefix="/arquivos")
app.register_blueprint(links_bp, url_prefix="/links")
app.register_blueprint(professores_bp, url_prefix="/professores")

if __name__ == "__main__":
    app.run(debug=True)
