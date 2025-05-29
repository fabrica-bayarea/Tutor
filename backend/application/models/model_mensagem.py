from application.config import db
import uuid
from datetime import datetime

class Mensagem(db.Model):
    __tablename__ = 'mensagens'

    id = db.Column(db.UUID(as_uuid=True, primary_key=True, default=uuid.uuid4))
    chat_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('chats.id'), nullable=False)
    sender_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('alunos.id'), nullable=False)
    conteudo = db.Column(db.String(3200), nullable=False)
    data_envio = db.Column(db.DateTime, nullable=False, default=datetime.now)
