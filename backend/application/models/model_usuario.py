from application.config.database import db
import uuid
import enum

class RoleEnum(enum.Enum):
    ADMIN = 1
    PROFESSOR = 2
    ALUNO = 3

class StatusEnum(enum.Enum):
    ATIVO = 1
    INATIVO = 2

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula = db.Column(db.String(10), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    senha = db.Column(db.String(256), nullable=False)
    # role e status usam enums distintos (GAP-02-K) — evita estados inválidos como
    # status=PROFESSOR. Como native_enum=False armazena o NOME, a separação não
    # exige migração de dados (os valores gravados continuam 'ATIVO'/'INATIVO').
    role = db.Column(db.Enum(RoleEnum, native_enum=False), nullable=False)
    status = db.Column(db.Enum(StatusEnum, native_enum=False), nullable=False)

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
            'role': self.role.name,
            'status': self.status.name
        }
