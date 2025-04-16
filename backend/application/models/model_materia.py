from application.config import db
import uuid

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.String(10), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(64), nullable=False)

    professores_responsaveis = db.relationship('ProfessorMateria', back_populates='materia', cascade='all, delete-orphan')
    turmas = db.relationship('TurmaMateria', back_populates='materia', cascade='all, delete-orphan')
    arquivos = db.relationship('ArquivoTurmaMateria', back_populates='materia')
