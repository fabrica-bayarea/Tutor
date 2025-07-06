from application.config.database import db
from application.models import Chat
import uuid

def criar_chat(aluno_id: uuid.UUID) -> dict:
    """
    Cria um novo chat para um aluno.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno

    Retorna o chat criado.
    """
    chat = Chat(aluno_id=aluno_id)
    db.session.add(chat)
    db.session.commit()

    return chat.to_dict()

def buscar_chats(aluno_id: uuid.UUID) -> list[dict] | None:
    """
    Busca TODOS os chats de um aluno.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno

    Retorna uma lista de chats.
    """
    chats = Chat.query.filter_by(aluno_id=aluno_id)
    return [chat.to_dict() for chat in chats.all()] if chats else None

def deletar_chat(chat_id: uuid.UUID) -> bool:
    """
    Deleta um chat.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat

    Retorna True se o chat for deletado com sucesso, e False se o chat não existir.
    """
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        return False
    
    db.session.delete(chat)
    db.session.commit()

    return True
