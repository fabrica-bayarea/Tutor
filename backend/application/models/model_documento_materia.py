from application.config import db

class DocumentoMateria(db.Model):
    """
    Entidade intermediária, responsável por lidar com relacionamentos entre Documentos e Matérias.
    """
    __tablename__ = 'documentos_materias'

    documento_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('documentos.id'), nullable=False, primary_key=True)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False, primary_key=True)

    documento = db.relationship('Documento', backref='materias', foreign_keys=[documento_id])
    materia = db.relationship('Materia', backref='documentos', foreign_keys=[materia_id])
