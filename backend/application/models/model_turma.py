from application.config import db
import uuid

class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.String(8), nullable=False, unique=True, index=True)
    semestre = db.Column(db.String(6), nullable=False)
    turno = db.Column(db.String(10), nullable=False)

    alunos_matriculados = db.relationship('AlunoTurma', back_populates='turma', cascade='all, delete-orphan')
    professores_materias = db.relationship('ProfessorTurmaMateria', back_populates='turma', cascade='all, delete-orphan')
    materias = db.relationship('TurmaMateria', back_populates='turma', cascade='all, delete-orphan')
    arquivos = db.relationship('ArquivoTurmaMateria', back_populates='turma')

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Turma em um dicionário serializável.

        Retorna um dicionário contendo as informações da turma.
        """
        return {
            'id': str(self.id),
            'codigo': self.codigo,
            'semestre': self.semestre,
            'turno': self.turno
        }
