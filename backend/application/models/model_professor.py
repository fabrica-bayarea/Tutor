from application.config import db
import uuid

class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula = db.Column(db.String(10), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    senha = db.Column(db.String(32), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True, index=True)
    data_nascimento = db.Column(db.Date, nullable=False)

    turmas_materias = db.relationship('ProfessorTurmaMateria', back_populates='professor', cascade='all, delete-orphan')

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Professor em um dicionário serializável.

        Retorna um dicionário contendo as informações do professor.
        """
        return {
            'id': str(self.id),
            'matricula': self.matricula,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento.strftime('%d/%m/%Y')
        }
