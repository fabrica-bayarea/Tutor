from flask_socketio import emit
from flask import request
from application.socket.Impl.registrar_chat import registrar_chat
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.socket.Impl.validacao_emit import validacao_emit
from application.socket.Impl.disparar_emit import disparar_emit
from application.mcp.server import call_tool_local
from application.socket.socket_instance import socketio

@socketio.on("connect")
def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})

@socketio.on('mensagem_inicial')
async def maestro(data: dict[str, str]):
    sid = request.sid

    # Realiza uma validação dos dados do payload recebido:
    await disparar_emit(socketio, 'processando',{}, sid)
    try:
        validacao_emit(data)
    except Exception as e:
        return await disparar_emit(socketio, "erro", {"erro": str(e)}, sid)
    
    # Inicializa as variaveis com os dados do paylaod
    usuario_id = data['id_usuario']
    materia_id = data['materia_id']
    mensagem = data['mensagem']
    historico_mensagens = data['historico']
    chat_novo = data['chat_novo']
    chat_id = data['id_chat']
    data_envio = data['data_envio']

    # Verifica a necessidade de criar um chat novo
    if chat_novo:
        try:
            chat_id = registrar_chat(usuario_id,materia_id,f"{usuario_id}-ChatTeste")
        except Exception as e:
            return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)
    
    # Salva a pergunta no banco de dados
    try:
        registrar_mensagem(chat_id,usuario_id,None,data_envio,mensagem) 
    except Exception as e:
        return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)
    
    # Criando prompt final
    if historico_mensagens is not None:
        historico_formatado = "\n".join(f"{m['sender']}: {m['content']}" for m in historico_mensagens)
    else:
        historico_formatado = ""

    # Posteriormente esta variavel será substituida pela lógica de busca de modelo por matéria.
    model = "ollama3"

    # Hardset matéria para develop
    materia = "Matemática"

    await call_tool_local(
        "chat",
        {
            "materia_id": materia_id,
            "mensagem": mensagem,
            "historico": historico_formatado,
            "sid": sid,
            "model": model,
            "materia": materia
        }
    )
