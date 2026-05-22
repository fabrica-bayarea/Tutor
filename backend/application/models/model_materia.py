from application.config.database import db
import uuid
from enum import Enum


class StatusMateriaEnum(Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.String(10), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(64), nullable=False)
    status = db.Column(db.Enum(StatusMateriaEnum, native_enum='ATIVO'), nullable=False)

    professores_turmas = db.relationship('ProfessorTurmaMateria', back_populates='materia', cascade='all, delete-orphan')
    turmas = db.relationship('TurmaMateria', back_populates='materia', cascade='all, delete-orphan')
    arquivos = db.relationship('ArquivoTurmaMateria', back_populates='materia')
    chats = db.relationship('Chat', back_populates='materia', cascade='all, delete-orphan')
    llm_id = db.Column(db.String, db.ForeignKey("llm.id"), nullable=True)
    llm = db.relationship("LLM", backref="materias")

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Materia em um dicionário serializável.

        Retorna um dicionário contendo as informações da matéria.
        """
        return {
            'id': str(self.id),
            'codigo': self.codigo,
            'nome': self.nome,
            'status': self.status.name
        }