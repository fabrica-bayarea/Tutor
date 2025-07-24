from application.config.database import db
from application.models import Mensagem
from application.services.service_aluno import buscar_aluno
from application.constants import LLM_UUID
import uuid

def criar_mensagem(chat_id: uuid.UUID, sender_id: uuid.UUID, conteudo: str, id: uuid.UUID = None) -> dict:
    """
    Cria uma nova mensagem.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat
    - `sender_id`: uuid.UUID - o ID do remetente
    - `conteudo`: str - o conteúdo da mensagem
    - `id`: uuid.UUID - o ID da mensagem (opcional)

    Retorna a mensagem criada.
    """
    aluno = buscar_aluno(sender_id)
    if not aluno and sender_id != LLM_UUID:
        raise ValueError("Aluno não encontrado")
    
    if id is not None:
        mensagem = Mensagem(id=id, chat_id=chat_id, sender_id=sender_id, conteudo=conteudo)
        db.session.add(mensagem)
        db.session.commit()
        return mensagem.to_dict()
    
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
    mensagens = Mensagem.query.filter_by(chat_id=chat_id)

    return [mensagem.to_dict() for mensagem in mensagens.all()] if mensagens else None

def buscar_ultimas_n_mensagens(chat_id: uuid.UUID, n: int = 20) -> list[dict]:
    """
    Busca as últimas N mensagens de um chat.

    Essa função é especialmente útil para fornecer o histórico recente de uma conversa como contexto para a LLM.

    Espera receber:
    - `chat_id`: uuid.UUID - o ID do chat
    - `n`: int - o número de mensagens a buscar (opcional)

    Se `n` não for informado, retorna as últimas 20 mensagens por padrão.

    Retorna uma lista de mensagens.
    """
    mensagens = Mensagem.query.filter_by(chat_id=chat_id).order_by(Mensagem.data_envio).limit(n)

    return [mensagem.to_dict() for mensagem in mensagens.all()] if mensagens else None

def atualizar_mensagem(id: uuid.UUID, novo_conteudo: str) -> dict:
    """
    Atualiza o conteúdo de uma mensagem.

    Espera receber:
    - `id`: uuid.UUID - o ID da mensagem
    - `novo_conteudo`: str - o novo conteúdo da mensagem

    Retorna a mensagem atualizada.
    """
    mensagem = Mensagem.query.filter_by(id=id).first()
    if not mensagem:
        raise ValueError("Mensagem não encontrada")
    
    mensagem.conteudo = novo_conteudo
    db.session.commit()
    
    return mensagem.to_dict()

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
