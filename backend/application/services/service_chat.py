from application.config.database import db
from application.models import Chat
import uuid
from datetime import datetime

def criar_chat(aluno_id: uuid.UUID, nome: str = None) -> dict:
    """
    Cria um novo chat para um aluno.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno
    - `nome`: str - o nome do chat

    Se um nome não for fornecido, a data e hora atual serão usadas como nome.

    Retorna o chat criado.
    """
    if nome is None:
        nome = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    chat = Chat(aluno_id=aluno_id, nome=nome)
    db.session.add(chat)
    db.session.commit()

    return chat.to_dict()

def buscar_chats(aluno_id: uuid.UUID) -> list[dict] | None:
    """
    Busca TODOS os chats de um aluno.

    Espera receber:
    - `aluno_id`: uuid.UUID - o ID do aluno

    Retorna uma lista de chats se existirem, e None caso contrário.
    """
    chats = Chat.query.filter_by(aluno_id=aluno_id)
    return [chat.to_dict() for chat in chats.all()] if chats else None

def buscar_chat(chat_id: uuid.UUID = None, aluno_id: uuid.UUID = None) -> dict | None:
    """
    Busca UM chat a partir de seu ID.

    Espera receber um ou ambos os parâmetros:
    - `chat_id`: uuid.UUID - o ID do chat
    - `aluno_id`: uuid.UUID - o ID do aluno

    Retorna o chat se ele existir, e None caso contrário.
    """
    if not any([chat_id, aluno_id]):
        raise ValueError("É obrigatório fornecer ao menos um ID de chat ou um ID de aluno.")
    
    chat = Chat.query
    
    if chat_id is not None:
        chat = chat.filter_by(id=chat_id)
    
    if aluno_id is not None:
        chat = chat.filter_by(aluno_id=aluno_id)
    
    return chat.to_dict() if chat.first() else None

def atualizar_chat(chat_id: uuid.UUID, novo_nome: str) -> dict | None:
    """
    Atualiza o nome de um chat.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat
    - `novo_nome`: str - o novo nome do chat

    Retorna o chat atualizado se ele existir, e None caso contrário.
    """
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        return None
    
    chat.nome = novo_nome
    db.session.commit()

    return chat.to_dict()

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
