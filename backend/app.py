from flask import Flask
from flask_migrate import Migrate
from application.config import *
from application.libs import *
from application.models import *
from application.routes import *
from application.services import *

app = Flask(__name__)
# init_db(app)
# migrate = Migrate(app, db)

collection = chroma_client.get_or_create_collection(name="documentos")

app.register_blueprint(documentos_bp, url_prefix="/documentos")
app.register_blueprint(links_bp, url_prefix="/links")
app.register_blueprint(videos_bp, url_prefix="/videos")

if __name__ == "__main__":
    app.run(debug=True)
