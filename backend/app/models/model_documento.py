from app.config import db
import uuid

class Documento(db.Model):
    __tablename__ = 'documentos'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professores.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
