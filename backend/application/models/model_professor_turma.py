from application.config import db

class ProfessorTurma(db.Model):
    """
    Entidade intermediária, responsável por lidar com relacionamentos entre Professores e Turmas.
    """
    __tablename__ = 'professores_turmas'

    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professores.id'), nullable=False, primary_key=True)
    turma_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('turmas.id'), nullable=False, primary_key=True)

    professor = db.relationship('Professor', back_populates='turmas_lecionadas')
    turma = db.relationship('Turma', back_populates='professores_regentes')
