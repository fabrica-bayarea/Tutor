from config import db
import uuid

class DocumentoMateria(db.Model):
    """Entidade intermediária, responsável por lidar com relacionamentos entre Documentos e Matérias."""
    __tablename__ = 'documentos_materias'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    documento_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('documentos.id'), nullable=False)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False)

    documento = db.relationship('Documento', backref='materias', foreign_keys=[documento_id])
    materia = db.relationship('Materia', backref='documentos', foreign_keys=[materia_id])
