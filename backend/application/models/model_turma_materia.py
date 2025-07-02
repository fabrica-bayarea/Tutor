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

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto TurmaMateria em um dicionário serializável.

        Retorna um dicionário contendo os IDs da turma e matéria como strings.
        """
        return {
            "turma_id": str(self.turma_id),
            "materia_id": str(self.materia_id)
        }
