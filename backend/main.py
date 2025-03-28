from flask import Flask
from flask_migrate import Migrate
from app.config import *
from app.models import *

app = Flask(__name__)
app.config.from_object(Config)

init_db(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
