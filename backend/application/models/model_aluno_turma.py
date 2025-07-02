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

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto AlunoTurma em um dicionário serializável.

        Retorna um dicionário contendo os IDs do aluno e turma como strings.
        """
        return {
            "aluno_id": str(self.aluno_id),
            "turma_id": str(self.turma_id)
        }
