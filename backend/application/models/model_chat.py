from application.config import db
import uuid

class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.UUID(as_uuid=True, primary_key=True, default=uuid.uuid4))
    aluno_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('alunos.id'), nullable=False)
    nome = db.Column(db.String(64), nullable=False)
