from application.config.database import db
import uuid
import enum

class RoleEnum(enum.Enum):
    ADMIN = 1
    PROFESSOR = 2
    ALUNO = 3

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula = db.Column(db.String(10), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    senha = db.Column(db.String(128), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)

    turmas_matriculadas = db.relationship('AlunoTurma', back_populates='aluno', cascade='all, delete-orphan')
    turmas_materias = db.relationship('ProfessorTurmaMateria', back_populates='professor', cascade='all, delete-orphan')
    chats = db.relationship('Chat', back_populates='aluno', cascade='all, delete-orphan')

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Aluno em um dicionário serializável.

        Retorna um dicionário contendo as informações do aluno.
        """
        return {
            'id': str(self.id),
            'matricula': self.matricula,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento.strftime('%d/%m/%Y'),
            'role': str(self.role)
        }
