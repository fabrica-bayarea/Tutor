from application.config import db
import uuid
from datetime import datetime

class Arquivo(db.Model):
    __tablename__ = 'arquivos'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professores.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)

    turmas_materias = db.relationship('ArquivoTurmaMateria', back_populates='arquivo')
