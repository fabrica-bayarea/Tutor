from flask_socketio import SocketIO, emit
from application.config.vector_database import collection
from application.services.service_chat import criar_chat
from application.services.service_mensagem import criar_mensagem
from application.constants import LLM_UUID
import ollama

socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")

@socketio.on("connect")
def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})

@socketio.on('mensagem_inicial')
def handle_mensagem_inicial(aluno_id, mensagem):
    """
    Função responsável por lidar com mensagens iniciais.

    Espera receber:
        - `aluno_id`: o ID do aluno que enviou a mensagem
        - `mensagem`: o conteúdo da mensagem

        1. Cria um novo chat usando o ID do aluno
        2. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
        3. Chama a LLM para gerar uma resposta
            3.1. Faz uma busca semântica no banco vetorial
            3.2. Gera a resposta
        4. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
        5. Envia o chat e a resposta para o front-end
    """
    #1. Cria um novo chat usando o ID do aluno
    chat = criar_chat(aluno_id)

    #2. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
    mensagem_aluno = criar_mensagem(chat.id, aluno_id, mensagem)
    
    #3. Chama a LLM para gerar uma resposta
    #3.1. Faz uma busca semântica no banco vetorial usando o conteúdo da mensagem do aluno
    contexts = collection.query(
        query_texts=[mensagem_aluno.conteudo],
        n_results=5,
    )

    #3.2. Gera a resposta
    emit("resposta_inicio", {"mensagem": ""})

    try:
        resposta_completa = ""
        for chunk in ollama.generate(
            model=LLM_UUID,
            prompt=f"""{mensagem_aluno.conteudo}
            
            Documentos:
            {contexts}""",
            stream=True,
            options={
                'num_predict': 512,
                'temperature': 0.7,
            }
        ):
            texto = chunk.get("response", "")
            print(f"Chunk: {texto}")
            resposta_completa += texto
            print(f"Estado atual da resposta: {resposta_completa}")

            emit("resposta_chunk", {"texto": texto})
        
        emit("resposta_fim", {"texto": resposta_completa})
    except Exception as e:
        emit("erro", {"mensagem": f"Erro ao gerar resposta: {str(e)}"})
    #4. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
    mensagem_llm = criar_mensagem(chat.id, LLM_UUID, resposta_completa)
    
    #5. Envia o chat e a resposta para o front-end
    emit("novo_chat", {
        "chat": chat,
        "mensagens": [
            mensagem_aluno,
            mensagem_llm
        ]
    })

@socketio.on('nova_mensagem')
def handle_nova_mensagem(chat_id, aluno_id, mensagem):
    """
    Função responsável por lidar com mensagens.

    Espera receber:
        - `chat_id`: o ID do chat que está recebendo a mensagem
        - `aluno_id`: o ID do aluno que enviou a mensagem
        - `mensagem`: o conteúdo da mensagem

        1. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat
        2. Chama a LLM para gerar uma resposta
        3. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat
        4. Envia a resposta para o front-end
    """
    pass
