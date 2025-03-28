from app.config import db
import uuid

class Documento(db.Model):
    __tablename__ = 'documentos'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professores.id'), nullable=False)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    materia = db.relationship('Materia', backref='documentos', foreign_keys=[materia_id])
    professor = db.relationship('Professor', backref='documentos', foreign_keys=[professor_id])
