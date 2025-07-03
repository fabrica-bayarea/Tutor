from flask_socketio import emit
from application.constants import LLM_UUID
from application.mistral.core import pipeline

def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})

def handle_mensagem_inicial(aluno_id, mensagem):
    """
    Função responsável por lidar com mensagens iniciais.

    Espera receber:
        - `aluno_id`: o ID do aluno que enviou a mensagem
        - `mensagem`: o conteúdo da mensagem

        1. Cria um novo chat usando o ID do aluno
        2. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
        3. Chama a LLM para gerar uma resposta
        4. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
        5. Envia o chat e a resposta para o front-end
    """
    pass

def handle_nova_mensagem(chat_id, aluno_id, mensagem):
    """
    Função responsável por lidar com mensagens.

    Espera receber:
        - `chat_id`: o ID do chat que está recebendo a mensagem
        - `aluno_id`: o ID do aluno que enviou a mensagem
        - `mensagem`: o conteúdo da mensagem

        1. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat
        2. Chama a LLM para gerar uma resposta
        4. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat
        5. Envia a resposta para o front-end
    """
    pass