from application.config.database import db

class AlunoTurma(db.Model):
    """
    Entidade intermediária, responsável por lidar com relacionamentos entre Alunos e Turmas.
    """
    __tablename__ = 'alunos_turmas'

    aluno_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('alunos.id'), nullable=False, primary_key=True)
    turma_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('turmas.id'), nullable=False, primary_key=True)

    aluno = db.relationship('Aluno', back_populates='turmas_matriculadas')
    turma = db.relationship('Turma', back_populates='alunos_matriculados')
