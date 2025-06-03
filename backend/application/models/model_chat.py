from application.config import db
import uuid

class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aluno_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('alunos.id'), nullable=False)
    nome = db.Column(db.String(64), nullable=False)

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Chat em um dicionário serializável.

        Retorna um dicionário contendo as informações do chat.
        """
        return {
            'id': str(self.id),
            'aluno_id': str(self.aluno_id),
            'nome': self.nome
        }
