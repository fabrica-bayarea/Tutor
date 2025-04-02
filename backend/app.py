from flask import Flask
from flask_migrate import Migrate
from app.config import *
from app.models import *

app = Flask(__name__)
init_db(app)
migrate = Migrate(app, db)

collection = chroma_client.get_or_create_collection(name="documentos")

if __name__ == "__main__":
    app.run(debug=True)
