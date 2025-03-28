from app.config import db
import uuid

class ProfessorMateria(db.Model):
    """Entidade intermediária, responsável por lidar com relacionamentos entre Professores e Matérias."""
    __tablename__ = 'professores_materias'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professores.id'), nullable=False)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False)

    professor = db.relationship('Professor', backref='materias', foreign_keys=[professor_id])
    materia = db.relationship('Materia', backref='professores', foreign_keys=[materia_id])
