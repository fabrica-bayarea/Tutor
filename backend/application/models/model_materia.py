from application.config import db
import uuid

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.String(10), nullable=False, unique=True)
    nome = db.Column(db.String(64), nullable=False)
