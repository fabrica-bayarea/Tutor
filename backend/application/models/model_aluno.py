from application.config import db
import uuid

class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula = db.Column(db.String(10), nullable=False, unique=True)
    nome = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    senha = db.Column(db.String(32), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    data_nascimento = db.Column(db.Date, nullable=False)

    turmas_matriculadas = db.relationship('AlunoTurma', back_populates='aluno', cascade='all, delete-orphan')
