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
    print(f"Chat criado:\n{chat}")

    #2. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
    mensagem_aluno = criar_mensagem(chat.id, aluno_id, mensagem)
    print(f"Mensagem salva:\n{mensagem_aluno}")
    
    #3. Chama a LLM para gerar uma resposta
    #3.1. Faz uma busca semântica no banco vetorial usando o conteúdo da mensagem do aluno
    contexts = collection.query(
        query_texts=[mensagem_aluno['conteudo']],
        n_results=5,
    )
    print(f"Contextos encontrados:\n{contexts}")

    #3.2. Gera a resposta
    emit("resposta_inicio", {"mensagem": ""})

    # Extrai os documentos dos contextos
    documentos = "\n\n".join([doc for doc in contexts.get('documents', [[]])[0]])
    
    prompt_llm = f"""
    Com base nas informações fornecidas nos trechos de documentos abaixo, responda ao comando do aluno.
    Se a resposta não estiver contida nos trechos fornecidos, responda APENAS "Não sei responder com base nas informações disponíveis".
    Formate a resposta em markdown com tags relevantes para títulos, parágrafos, listas e etc.

    Trechos de documentos:
    {documentos}

    Comando do aluno: {mensagem_aluno['conteudo']}
    """

    try:
        resposta_completa = ""
        print("Enviando requisição para a LLM...")
        
        response = ollama.generate(
            model="mistral",
            prompt=prompt_llm,
            stream=True,
            options={
                'num_predict': 512,
                'temperature': 0.7,
            }
        )
        
        print("Recebendo resposta da LLM...")
        
        for chunk in response:
            texto = chunk.get("response", "")
            print(f"Chunk recebido: {texto}")
            if texto:
                resposta_completa += texto
                emit("resposta_chunk", {"texto": texto})
        
        print(f"Resposta completa: {resposta_completa}")
        
        if not resposta_completa.strip():
            raise ValueError("A resposta da LLM está vazia")
            
        emit("resposta_fim", {"texto": resposta_completa})
        
    except Exception as e:
        error_msg = f"Erro ao gerar resposta: {str(e)}"
        print(error_msg)
        emit("erro", {"mensagem": error_msg})
        return

    #4. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
    mensagem_llm = criar_mensagem(chat.id, LLM_UUID, resposta_completa)
    print(f"Resposta da LLM salva:\n{mensagem_llm}")
    
    #5. Envia o chat e a resposta para o front-end
    print(f"Chat e resposta enviados para o front-end:\n{chat}\n{mensagem_llm}")
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
    
    #1. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
    mensagem_aluno = criar_mensagem(chat_id, aluno_id, mensagem)
    print(f"Mensagem salva:\n{mensagem_aluno}")
    print(f"Conteúdo da mensagem do aluno (`mensagem_aluno['conteudo']`): {mensagem_aluno['conteudo']}")
    
    #2. Chama a LLM para gerar uma resposta
    #2.1. Faz uma busca semântica no banco vetorial usando o conteúdo da mensagem do aluno
    contexts = collection.query(
        query_texts=[mensagem_aluno['conteudo']],
        n_results= 5
    )
    print(f"Contextos encontrados:\n{contexts}")    

    #2.2. Gera a resposta
    emit("resposta_inicio", {"mensagem": ""})

    # Extrai os documentos dos contextos
    documentos = "\n\n".join([doc for doc in contexts.get('documents', [[]])[0]])
    
    prompt_llm = f"""
    Com base nas informações fornecidas nos trechos de documentos abaixo, responda ao comando do aluno.
    Se a resposta não estiver contida nos trechos fornecidos, responda APENAS "Não sei responder com base nas informações disponíveis".
    Formate a resposta em markdown com tags relevantes para títulos, parágrafos, listas e etc.

    Trechos de documentos:
    {documentos}

    Comando do aluno: {mensagem_aluno['conteudo']}
    """
    print(f"Prompt para a LLM:\n{prompt_llm}")

    try:
        resposta_completa = ""
        print("Enviando requisição para a LLM...")
        
        response = ollama.generate(
            model="mistral",
            prompt=prompt_llm,
            stream=True,
            options={
                'num_predict': 512,
                'temperature': 0.7,
            }
        )
        
        print("Recebendo resposta da LLM...")
        
        for chunk in response:
            texto = chunk.get("response", "")
            print(f"Chunk recebido: {texto}")
            if texto:
                resposta_completa += texto
                emit("resposta_chunk", {"texto": texto})
        
        print(f"Resposta completa: {resposta_completa}")
        
        if not resposta_completa.strip():
            raise ValueError("A resposta da LLM está vazia")
            
        emit("resposta_fim", {"texto": resposta_completa})
        
    except Exception as e:
        error_msg = f"Erro ao gerar resposta: {str(e)}"
        print(error_msg)
        emit("erro", {"mensagem": error_msg})
        return

    #3. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
    mensagem_llm = criar_mensagem(chat_id, LLM_UUID, resposta_completa)
    print(f"Resposta da LLM salva:\n{mensagem_llm}") 
    
    #4. Envia a resposta para o front-end
    emit("nova_mensagem_resposta", mensagem_llm)
