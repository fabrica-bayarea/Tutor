from application.config import db
import uuid

class AlunoMateria(db.Model):
    """Entidade intermediária, responsável por lidar com relacionamentos entre Alunos e Matérias."""
    __tablename__ = 'alunos_materias'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aluno_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('alunos.id'), nullable=False)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False)

    aluno = db.relationship('Aluno', backref='materias', foreign_keys=[aluno_id])
    materia = db.relationship('Materia', backref='alunos', foreign_keys=[materia_id])
