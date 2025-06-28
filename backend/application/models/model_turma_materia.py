from application.config.database import db

class TurmaMateria(db.Model):
    """
    Entidade intermediária, responsável por lidar com relacionamentos entre Turmas e Matérias.
    """
    __tablename__ = 'turmas_materias'

    turma_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('turmas.id'), nullable=False, primary_key=True)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False, primary_key=True)

    turma = db.relationship('Turma', back_populates='materias')
    materia = db.relationship('Materia', back_populates='turmas')
