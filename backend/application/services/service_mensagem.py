from application.config.database import db
from application.models import Mensagem
from application.services.service_aluno import buscar_aluno
from application.constants import LLM_UUID
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
    aluno = buscar_aluno(sender_id)
    if not aluno and sender_id != LLM_UUID:
        raise ValueError("Aluno não encontrado")
    
    mensagem = Mensagem(chat_id=chat_id, sender_id=sender_id, conteudo=conteudo)
    db.session.add(mensagem)
    db.session.commit()

    return mensagem.to_dict()

def buscar_mensagens(chat_id: uuid.UUID) -> list[Mensagem]:
    """
    Busca TODAS as mensagens de um chat.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat

    Retorna uma lista de mensagens.
    """
    mensagens = Mensagem.query.filter_by(chat_id=chat_id).all()

    return [mensagem.to_dict() for mensagem in mensagens] if mensagens else None

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
