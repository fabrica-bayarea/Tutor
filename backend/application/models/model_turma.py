from application.config import db
import uuid

class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.String(8), nullable=False)
    semestre = db.Column(db.String(8), nullable=False)
    turno = db.Column(db.String(6), nullable=False)
