from application.config import db
import uuid

class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.String(8), nullable=False, unique=True, index=True)
    semestre = db.Column(db.String(6), nullable=False)
    turno = db.Column(db.String(10), nullable=False)

    alunos_matriculados = db.relationship('AlunoTurma', back_populates='turma', cascade='all, delete-orphan')
    professores_regentes = db.relationship('ProfessorTurma', back_populates='turma', cascade='all, delete-orphan')
    materias = db.relationship('TurmaMateria', back_populates='turma', cascade='all, delete-orphan')
    arquivos = db.relationship('ArquivoTurmaMateria', back_populates='turma')
