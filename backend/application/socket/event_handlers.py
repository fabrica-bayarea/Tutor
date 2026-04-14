from flask_socketio import SocketIO, emit, request
from application.socket.Impl.registrar_chat import registrar_chat
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.socket.Impl.validacao_emit import validacao_emit
from application.socket.Impl.disparar_emit import disparar_emit
from application.socket.Impl.gerar_resposta_llm import gerar_resposta_llm

socketio = SocketIO(cors_allowed_origins="*", async_mode="gevent")

@socketio.on("connect")
def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})

@socketio.on('mensagem_inicial')
def maestro(data: dict[str, str]):
    sid = request.sid

    # Realiza uma validação dos dados do payload recebido:
    disparar_emit(socketio, 'processando',{}, sid)
    try:
        validacao_emit(data)
    except Exception as e:
        return disparar_emit(socketio,"erro",{},sid)
    
    # Inicializa as variaveis com os dados do paylaod
    usuario_id = data['id_usuario']
    materia_id = data['materia_id']
    chat_id = data['id_chat']
    historico_mensagens = data['historico']
    chat_novo = data['chat_novo']
    data_envio = data['data_envio']
    mensagem = data['mensagem']
    # sessao = data['sessao']

    # Verifica a necessidade de criar um chat novo
    if chat_novo:
        try:
            chat_id = registrar_chat(usuario_id,materia_id,"Teste")
        except Exception as e:
            return disparar_emit(socketio,"erro",{},sid)
    
    # Salva a pergunta no banco de dados
    try:
        mensagem_id = registrar_mensagem(chat_id,usuario_id,sid,data_envio,mensagem) #adicionar a sessão ao paylaod
    except Exception as e:
        return disparar_emit(socketio,"erro",{},sid)
    
    # Criando prompt final
    if historico_mensagens is not None:
        historico_formatado = "\n".join(f"{m['sender']}: {m['content']}" for m in historico_mensagens)
    else:
        historico_formatado = ""

    prompt_final = f"""Com base nas informações fornecidas nos trechos de documentos abaixo, responda ao comando do aluno.
        Formate a resposta em markdown com tags relevantes para títulos, parágrafos, listas e etc.
        <historico_chat>
        # Comando do aluno. Use para responder ao aluno.
        {historico_formatado}
        </historico_chat>
        <comando_usuario>
        # Comando do usuario. Use para responder a ele.
        {mensagem}
        </comando_usuario>
    """

    # Gerar a resposta
    disparar_emit(socketio, 'gerando resposta',{}, sid)
    gerar_resposta_llm(prompt_final,None,socketio,mensagem_id,chat_id,sid)

    
