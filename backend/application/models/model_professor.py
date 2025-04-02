from application.config import db
import uuid

class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula = db.Column(db.String(100), nullable=False, unique=True)
    nome = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    senha = db.Column(db.String(32), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
