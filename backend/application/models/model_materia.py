from application.config.database import db
import uuid

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.String(10), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(64), nullable=False)

    professores_turmas = db.relationship('ProfessorTurmaMateria', back_populates='materia', cascade='all, delete-orphan')
    turmas = db.relationship('TurmaMateria', back_populates='materia', cascade='all, delete-orphan')
    arquivos = db.relationship('ArquivoTurmaMateria', back_populates='materia')

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Materia em um dicionário serializável.

        Retorna um dicionário contendo as informações da matéria.
        """
        return {
            'id': str(self.id),
            'codigo': self.codigo,
            'nome': self.nome
        }
