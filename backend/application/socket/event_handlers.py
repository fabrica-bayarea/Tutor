from flask import request
from flask_socketio import SocketIO, emit
from application.config.vector_database import collection
from application.services.service_chat import criar_chat
from application.services.service_mensagem import criar_mensagem, buscar_ultimas_n_mensagens
from application.libs.mistral_handler import contar_tokens_mensagens
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
    prompt_nome_chat = f"""Você é um assistente que precisa criar um nome curto, objetivo e DESCRITIVO para um chat, com base na pergunta abaixo. O nome deve:

- Ser em **português**
- Ter no máximo **64 caracteres**
- Ter apenas UMA linha
- Ser formatado como **título com espaços** (não junte as palavras)
- NÃO inclua pontuação ou aspas
- Responda APENAS com o nome gerado (sem explicações)

<pergunta_aluno>
{mensagem}
</pergunta_aluno>
"""
    response_nome_chat = ollama.generate(
        model="mistral",
        prompt=prompt_nome_chat,
        stream=False,
        options={
            'num_predict': 16,
            'temperature': 0.7,
        }
    ).get("response", "")
    print(f"Nome criado para o chat: {response_nome_chat}")
    chat = criar_chat(aluno_id, response_nome_chat)
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

<documentos_relevantes>
# Documentos recuperados por busca semântica. Use para enriquecer a resposta com dados objetivos.
{documentos}
</documentos_relevantes>

<comando_aluno>
# Comando do aluno. Use para responder ao aluno.
{mensagem_aluno['conteudo']}
</comando_aluno>
"""
        print(f"Prompt para a LLM:\n{prompt_llm}")

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

        #2.2. Busca as N mensagens mais recentes do chat até atingir o limite de tokens
        n_mensagens = 20
        total_tokens = 0
        limite_tokens = 4096
        mensagens_para_tokenizer = []
        ha_mais_mensagens = True # Evita loops infinitos

        while total_tokens < limite_tokens and ha_mais_mensagens:
            mensagens_recentes = buscar_ultimas_n_mensagens(chat_id, n_mensagens)
            print(f"Mensagens recentes encontradas:\n{mensagens_recentes}")

            # Se a quantidade de mensagens retornadas for menor que a quantidade solicitada, significa que não há mais mensagens
            if len(mensagens_recentes) < n_mensagens:
                ha_mais_mensagens = False

            mensagens_para_tokenizer.extend([
                {"role": "user", "content": m["conteudo"]} if m["sender_id"] == aluno_id else
                {"role": "assistant", "content": m["conteudo"]}
                for m in mensagens_recentes
            ])
            print(f"Mensagens para tokenização:\n{mensagens_para_tokenizer}")

            total_tokens += contar_tokens_mensagens(mensagens_para_tokenizer)
            print(f"Total de tokens: {total_tokens}")
        
        prompt_rag = f"""
Você é um assistente que decide se uma pergunta pode ser respondida apenas com base na conversa anterior com o usuário, ou se precisa consultar documentos externos para dar uma resposta precisa (como materiais didáticos, textos técnicos ou artigos em uma base de conhecimento).

<mensagem_usuario>
{mensagem_aluno['conteudo']}
</mensagem_usuario>

<conversa_anterior>
{mensagens_para_tokenizer}
</conversa_anterior>

Se a resposta à pergunta do usuário pode ser dada com base apenas na conversa anterior, responda com "N".

Se for necessário consultar documentos externos para responder corretamente, responda com "S".

Responda APENAS com a letra S ou N.
"""
        print(f"Prompt para decisão de RAG:\n{prompt_rag}")

        resposta_rag = ollama.generate(
            model="mistral",
            prompt=prompt_rag,
            stream=False,
            options={
                'num_predict': 1,
                'temperature': 0.0,
            }
        ).get("response", "")
        print(f"Resposta da decisão de RAG: '{resposta_rag}'")

        documentos = ""
        if resposta_rag.strip() == "S":
            #2.3. Faz uma busca semântica no banco vetorial usando o conteúdo da mensagem do aluno
            contexts = collection.query(
                query_texts=[mensagem_aluno['conteudo']],
                n_results= 5
            )
            #print(f"Contextos encontrados:\n{contexts}")    

            #2.4. Extrai os documentos dos contextos
            documentos = "\n\n".join([doc for doc in contexts.get('documents', [[]])[0]])
        
        if documentos and documentos.strip():
            documentos_section = f"<documentos_relevantes>\n{documentos}\n</documentos_relevantes>"
        else:
            documentos_section = ""
        
        #2.5. Gera o prompt para a LLM
        prompt_llm = f"""
<mensagens_recentes>
# Histórico recente da conversa. Use para manter o tom e o contexto do usuário.
{mensagens_para_tokenizer}
</mensagens_recentes>

{documentos_section}

<comando_aluno>
# Comando do aluno. Use para responder ao aluno.
{mensagem_aluno['conteudo']}
</comando_aluno>
"""
        print(f"Prompt para a LLM:\n{prompt_llm}")

        resposta_completa = ""
        print("Enviando requisição para a LLM...")
        
        #2.6. Gera a resposta da LLM
        response = ollama.generate(
            model="mistral",
            prompt=prompt_llm,
            stream=True,
            options={
                #'num_predict': 512,
                'temperature': 0.7,
            }
        )
        
        print("Recebendo resposta da LLM...")
        
        #2.7. Pega e emite cada um dos chunks gerados
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
