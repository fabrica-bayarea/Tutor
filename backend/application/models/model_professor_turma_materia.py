from application.config.database import db

class ProfessorTurmaMateria(db.Model):
    __tablename__ = 'professores_turmas_materias'

    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('professores.id'), nullable=False, primary_key=True)
    turma_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('turmas.id'), nullable=False, primary_key=True)
    materia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('materias.id'), nullable=False, primary_key=True)

    professor = db.relationship('Professor', back_populates='turmas_materias')
    turma = db.relationship('Turma', back_populates='professores_materias')
    materia = db.relationship('Materia', back_populates='professores_turmas')
    
    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto ProfessorTurmaMateria em um dicionário serializável.

        Retorna um dicionário contendo os IDs do professor, turma e matéria como strings.
        """
        return {
            "professor_id": str(self.professor_id),
            "turma_id": str(self.turma_id),
            "materia_id": str(self.materia_id)
        }
