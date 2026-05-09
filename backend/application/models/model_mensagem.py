from application.config.database import db
import uuid
from datetime import datetime
from sqlalchemy.sql import func

class Mensagem(db.Model):
    __tablename__ = 'mensagens'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = db.Column(db.UUID(as_uuid=True),db.ForeignKey("chats.id"),nullable=False)
    sessao_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('sessao.id'))
    sender_id = db.Column(db.UUID(as_uuid=True), nullable=True)
    sender_type = db.Column(db.String(8), nullable=False, default='user')
    conteudo = db.Column(db.String(3200), nullable=False)
    data_envio = db.Column(db.DateTime, nullable=False, server_default=func.now())

    chat = db.relationship("Chat", back_populates="mensagens")
    sessao = db.relationship("Sessao")

    def to_dict(self):
        """
        Função atômica, responsável por converter um objeto Mensagem em um dicionário serializável.

        Retorna um dicionário contendo as informações da mensagem.
        """
        return {
            'id': str(self.id),
            'chat_id': str(self.chat_id),
            'sessao_id': str(self.sessao_id),
            'sender_id': str(self.sender_id) if self.sender_id else None,
            'sender_type': self.sender_type,
            'conteudo': self.conteudo,
            'data_envio': self.data_envio.strftime('%d/%m/%Y %H:%M:%S')
        }
