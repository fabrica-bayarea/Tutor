from application.models import Mensagem
import uuid

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
