from flask import request
from flask_socketio import SocketIO, emit
from application.config.vector_database import collection
from application.services.service_chat import criar_chat
from application.services.service_mensagem import criar_mensagem
from application.constants import LLM_UUID
import uuid
import ollama

socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")

pendentes = {}

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
        3. Armazena ambos no dicionário `pendentes` para emitir em outros eventos após receber o "handshake" do front-end
    """
    sid = request.sid

    aluno_id = data['aluno_id']
    mensagem = data['mensagem']

    #1. Cria um novo chat usando o ID do aluno
    chat = criar_chat(aluno_id)
    print(f"Chat criado:\n{chat}")
    socketio.emit("novo_chat", chat, to=sid)
    socketio.sleep(0)
    
    #2. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
    mensagem_aluno = criar_mensagem(chat['id'], aluno_id, mensagem)
    print(f"Mensagem salva:\n{mensagem_aluno}")

    #3. Salva temporariamente pra emitir em outro evento
    pendentes[sid] = {
        "chat": chat,
        "mensagem": mensagem_aluno
    }

@socketio.on('pronto_para_receber')
def handle_pronto_para_receber():
    """
    Função responsável por lidar com os eventos subsequentes após receber o "handshake" do front-end.

    1. Emite a mensagem inicial enviada pelo aluno, armazenada em `pendentes`
    2. Gera a resposta da LLM.
    """
    sid = request.sid
    dados = pendentes.get(sid)
    
    if not dados:
        print(f'Nenhum dado para o socket {sid}')
        return
    
    chat = dados['chat']
    mensagem_aluno = dados['mensagem']

    print(f"Cliente pronto para receber. Emitindo mensagem e iniciando resposta para chat {chat['id']}")
    
    #1. Emite a mensagem inicial enviada pelo aluno, armazenada em `pendentes`
    socketio.emit("mensagem_aluno", mensagem_aluno, to=sid)
    socketio.sleep(0)
    
    try:
        #2. Gera uma resposta com a LLM
        #2.1. Gera e emite um ID para a mensagem da LLM
        id_mensagem_llm = uuid.uuid4()
        socketio.emit("resposta_inicio", str(id_mensagem_llm), to=sid)
        socketio.sleep(0)

        #2.2. Faz uma busca semântica no banco vetorial usando o conteúdo da mensagem do aluno
        contexts = collection.query(
            query_texts=[mensagem_aluno['conteudo']],
            n_results=5,
        )
        print(f"Contextos encontrados:\n{contexts}")
        
        #2.3. Extrai os documentos dos contextos
        documentos = "\n\n".join([doc for doc in contexts.get('documents', [[]])[0]])
        
        #2.4. Gera o prompt para a LLM
        prompt_llm = f"""
        Com base nas informações fornecidas nos trechos de documentos abaixo, responda ao comando do aluno.
        Se a resposta não estiver contida nos trechos fornecidos, responda APENAS "Não sei responder com base nas informações disponíveis".
        Formate a resposta em markdown com tags relevantes para títulos, parágrafos, listas e etc.

        Trechos de documentos:
        {documentos}

        Comando do aluno: {mensagem_aluno['conteudo']}
        """

        resposta_completa = ""
        print("Enviando requisição para a LLM...")
        
        #2.5. Gera a resposta da LLM
        response = ollama.generate(
            model="mistral",
            prompt=prompt_llm,
            stream=True,
            options={
                # 'num_predict': 512,
                'temperature': 0.7,
            }
        )
        
        print("Recebendo resposta da LLM...")
        
        #2.6. Pega e emite cada um dos chunks gerados
        for chunk in response:
            texto = chunk.get("response", "")
            print(f"Chunk recebido: {texto}")
            if texto:
                resposta_completa += texto
                socketio.emit("resposta_chunk", texto, to=request.sid)
                print(f"Chunk emitido: {texto}")
                socketio.sleep(0)
        
        print(f"Resposta completa: {resposta_completa}")
        
        if not resposta_completa.strip():
            raise ValueError("A resposta da LLM está vazia")
    
    except Exception as e:
        error_msg = f"Erro ao gerar resposta: {str(e)}"
        print(error_msg)
        socketio.emit("erro", {"mensagem": error_msg}, to=request.sid)
        return
    
    #3. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
    mensagem_llm = criar_mensagem(chat['id'], LLM_UUID, resposta_completa)
    print(f"Resposta da LLM salva:\n{mensagem_llm}") 
    
    #4. Envia a resposta para o front-end
    socketio.emit("resposta_fim", mensagem_llm, to=sid)
    socketio.sleep(0)

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
    sid = request.sid

    chat_id = data['chat_id']
    aluno_id = data['aluno_id']
    mensagem = data['mensagem']
    
    #1. Salva a mensagem no banco de dados relacional usando o ID do aluno e o ID do chat criado
    mensagem_aluno = criar_mensagem(chat_id, aluno_id, mensagem)
    print(f"Mensagem salva:\n{mensagem_aluno}")
    socketio.emit("res_mensagem", mensagem_aluno, to=sid)
    socketio.sleep(0)
    
    try:
        #2. Gera uma resposta com a LLM
        #2.1. Gera e emite um ID para a mensagem da LLM
        id_mensagem_llm = uuid.uuid4()
        socketio.emit("resposta_inicio", str(id_mensagem_llm), to=sid)
        socketio.sleep(0)

        #2.2. Faz uma busca semântica no banco vetorial usando o conteúdo da mensagem do aluno
        contexts = collection.query(
            query_texts=[mensagem_aluno['conteudo']],
            n_results= 5
        )
        print(f"Contextos encontrados:\n{contexts}")    

        #2.3. Extrai os documentos dos contextos
        documentos = "\n\n".join([doc for doc in contexts.get('documents', [[]])[0]])
        
        #2.4. Gera o prompt para a LLM
        prompt_llm = f"""
        Com base nas informações fornecidas nos trechos de documentos abaixo, responda ao comando do aluno.
        Se a resposta não estiver contida nos trechos fornecidos, responda APENAS "Não sei responder com base nas informações disponíveis".
        Formate a resposta em markdown com tags relevantes para títulos, parágrafos, listas e etc.

        Trechos de documentos:
        {documentos}

        Comando do aluno: {mensagem_aluno['conteudo']}
        """

        resposta_completa = ""
        print("Enviando requisição para a LLM...")
        
        #2.5. Gera a resposta da LLM
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
        
        #2.6. Pega e emite cada um dos chunks gerados
        for chunk in response:
            texto = chunk.get("response", "")
            print(f"Chunk recebido: {texto}")
            if texto:
                resposta_completa += texto
                socketio.emit("resposta_chunk", texto, to=sid)
                socketio.sleep(0)
        
        print(f"Resposta completa: {resposta_completa}")
        
        if not resposta_completa.strip():
            raise ValueError("A resposta da LLM está vazia")
    
    except Exception as e:
        error_msg = f"Erro ao gerar resposta: {str(e)}"
        print(error_msg)
        socketio.emit("erro", {"mensagem": error_msg}, to=sid)
        return

    #3. Salva a resposta da LLM no banco de dados relacional usando o ID da LLM e o ID do chat criado
    mensagem_llm = criar_mensagem(chat_id, LLM_UUID, resposta_completa)
    print(f"Resposta da LLM salva:\n{mensagem_llm}") 
    
    #4. Envia a resposta para o front-end
    socketio.emit("resposta_fim", mensagem_llm, to=sid)
    socketio.sleep(0)
