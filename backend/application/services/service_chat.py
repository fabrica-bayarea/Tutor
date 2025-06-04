from application.config import db
from application.models import Chat
import uuid

def criar_chat(aluno_id: uuid.UUID) -> Chat:
    """
    Cria um novo chat para um aluno.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno

    Retorna o chat criado.
    """
    chat = Chat(aluno_id=aluno_id)
    db.session.add(chat)
    db.session.commit()

    return chat

def buscar_chats(aluno_id: uuid.UUID) -> list[Chat]:
    """
    Busca TODOS os chats de um aluno.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno

    Retorna uma lista de chats.
    """
    query = Chat.query.filter_by(aluno_id=aluno_id)

    return query.all()

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
