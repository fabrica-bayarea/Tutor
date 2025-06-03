from application.config import db
from application.models import Mensagem
import uuid

def criar_mensagem(chat_id: uuid.UUID, sender_id: uuid.UUID, conteudo: str) -> Mensagem:
    """
    Cria uma nova mensagem.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat
    - `sender_id`: uuid.UUID - o ID do remetente
    - `conteudo`: str - o conteúdo da mensagem

    Retorna a mensagem criada.
    """
    mensagem = Mensagem(chat_id=chat_id, sender_id=sender_id, conteudo=conteudo)
    db.session.add(mensagem)
    db.session.commit()

    return mensagem

def buscar_mensagens(chat_id: uuid.UUID) -> list[Mensagem]:
    """
    Busca TODAS as mensagens de um chat.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat

    Retorna uma lista de mensagens.
    """
    query = Mensagem.query.filter_by(chat_id=chat_id)

    return query.all()

def deletar_mensagens(chat_id: uuid.UUID) -> bool:
    """
    Deleta TODAS as mensagens de um chat.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat

    Retorna True se as mensagens forem deletadas com sucesso, e False se o chat não existir.
    """
    query = Mensagem.query.filter_by(chat_id=chat_id)
    if not query.first():
        return False
    
    query.delete()
    db.session.commit()

    return True
