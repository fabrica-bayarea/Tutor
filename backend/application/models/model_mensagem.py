from application.config.database import db
import uuid
from datetime import datetime

class Mensagem(db.Model):
    __tablename__ = 'mensagens'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('chats.id'), nullable=False)
    sender_id = db.Column(db.UUID(as_uuid=True), nullable=False)
    conteudo = db.Column(db.String(3200), nullable=False)
    data_envio = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Mensagem em um dicionário serializável.

        Retorna um dicionário contendo as informações da mensagem.
        """
        return {
            'id': str(self.id),
            'chat_id': str(self.chat_id),
            'sender_id': str(self.sender_id),
            'conteudo': self.conteudo,
            'data_envio': self.data_envio.strftime('%d/%m/%Y %H:%M:%S')
        }
