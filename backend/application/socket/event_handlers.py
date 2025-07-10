from flask import request
from flask_socketio import SocketIO, emit
from application.config.vector_database import collection
from application.services.service_chat import criar_chat
from application.services.service_mensagem import criar_mensagem, atualizar_mensagem
from application.constants import LLM_UUID
from datetime import datetime
import uuid
import ollama

socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")

@socketio.on("connect")
def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})

@socketio.on('mensagem_inicial')
def handle_mensagem_inicial(data: dict[str, str]):
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
    print(f"Dados recebidos:\n{data}")
    aluno_id = data['aluno_id']
    mensagem = data['mensagem']
    #1. Cria um novo chat usando o ID do aluno
    chat = criar_chat(aluno_id)
    print(f"Chat criado:\n{chat}")
    socketio.emit("novo_chat", chat, to=request.sid)

    # Faz o socket dormir para que o front-end consiga processar o que recebeu
    socketio.sleep(0)
    
    #2. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
    mensagem_aluno = criar_mensagem(chat['id'], aluno_id, mensagem)
    print(f"Mensagem salva:\n{mensagem_aluno}")
    socketio.emit("mensagem_aluno", mensagem_aluno, to=request.sid)
    socketio.sleep(0)
    
    #3. Gera uma resposta com a LLM
    #3.1. Cria uma nova mensagem no banco de dados, inicialmente sem conteúdo (pois a LLM ainda não gerou)
    mensagem_llm = criar_mensagem(chat['id'], LLM_UUID, '')
    print(f"Mensagem da LLM salva:\n{mensagem_llm}")
    socketio.emit("resposta_inicio", mensagem_llm, to=request.sid)
    socketio.sleep(0)

    #3.2. Faz uma busca semântica no banco vetorial usando o conteúdo da mensagem do aluno
    contexts = collection.query(
        query_texts=[mensagem_aluno['conteudo']],
        n_results=5,
    )
    print(f"Contextos encontrados:\n{contexts}")
    
    #3.3. Extrai os documentos dos contextos
    documentos = "\n\n".join([doc for doc in contexts.get('documents', [[]])[0]])
    
    #3.4. Gera o prompt para a LLM
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
                socketio.emit("resposta_chunk", texto, to=request.sid)
                socketio.sleep(0)
        
        print(f"Resposta completa: {resposta_completa}")
        
        if not resposta_completa.strip():
            raise ValueError("A resposta da LLM está vazia")
    
    except Exception as e:
        error_msg = f"Erro ao gerar resposta: {str(e)}"
        print(error_msg)
        socketio.emit("erro", {"mensagem": error_msg}, to=request.sid)
        return
    
    #4. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
    mensagem_llm_atualizada = atualizar_mensagem(mensagem_llm['id'], resposta_completa)
    print(f"Resposta da LLM salva:\n{mensagem_llm_atualizada}")
    
    #5. Envia a resposta para o front-end
    socketio.emit("resposta_fim", mensagem_llm_atualizada, to=request.sid)
    print(f"Resposta enviada para o front-end:\n{mensagem_llm_atualizada}")

@socketio.on('nova_mensagem_aluno')
def handle_nova_mensagem(data: dict[str, str]):
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
    chat_id = data['chat_id']
    aluno_id = data['aluno_id']
    mensagem = data['mensagem']
    
    #1. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
    mensagem_aluno = criar_mensagem(chat_id, aluno_id, mensagem)
    print(f"Mensagem salva:\n{mensagem_aluno}")
    print(f"Conteúdo da mensagem do aluno (`mensagem_aluno['conteudo']`): {mensagem_aluno['conteudo']}")
    socketio.emit("res_mensagem", mensagem_aluno, to=request.sid)
    socketio.sleep(0)
    
    #2. Chama a LLM para gerar uma resposta
    #2.1. Faz uma busca semântica no banco vetorial usando o conteúdo da mensagem do aluno
    contexts = collection.query(
        query_texts=[mensagem_aluno['conteudo']],
        n_results= 5
    )
    print(f"Contextos encontrados:\n{contexts}")    

    #2.2. Gera a resposta
    resposta_llm = {
        'id': str(uuid.uuid4()),
        'chat_id': chat_id,
        'sender_id': str(LLM_UUID),
        'conteudo': '',
        'data_envio': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    socketio.emit("resposta_inicio", resposta_llm, to=request.sid)
    socketio.sleep(0)

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
                socketio.emit("resposta_chunk", texto, to=request.sid)
                socketio.sleep(0)
        
        print(f"Resposta completa: {resposta_completa}")
        
        if not resposta_completa.strip():
            raise ValueError("A resposta da LLM está vazia")
            
        socketio.emit("resposta_fim", resposta_llm, to=request.sid)
        socketio.sleep(0)
        
    except Exception as e:
        error_msg = f"Erro ao gerar resposta: {str(e)}"
        print(error_msg)
        socketio.emit("erro", {"mensagem": error_msg}, to=request.sid)
        return

    #3. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
    mensagem_llm = criar_mensagem(chat_id, LLM_UUID, resposta_completa)
    print(f"Resposta da LLM salva:\n{mensagem_llm}") 
    
    #4. Envia a resposta para o front-end
    socketio.emit("nova_resposta_completa", mensagem_llm, to=request.sid)
