from application.config import db

class ProfessorMateria(db.Model):
    """
    Entidade intermediária, responsável por lidar com relacionamentos entre Professores e Matérias.
    """
    __tablename__ = 'professores_materias'

    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professores.id'), nullable=False, primary_key=True)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False, primary_key=True)

    professor = db.relationship('Professor', back_populates='materias_lecionadas')
    materia = db.relationship('Materia', back_populates='professores_responsaveis')
