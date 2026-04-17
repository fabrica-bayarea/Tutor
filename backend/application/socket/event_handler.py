from flask_socketio import emit
from flask import request
from application.socket.Impl.registrar_chat import registrar_chat
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.socket.Impl.validacao_emit import validacao_emit
from application.socket.Impl.disparar_emit import disparar_emit
from application.mcp.server import call_tool_local
from application.socket.socket_instance import socketio
from threading import Thread

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
        return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)
    
    # Inicializa as variaveis com os dados do paylaod
    usuario_id = data['id_usuario']
    materia_id = data['materia_id']
    chat_id = data['id_chat']
    historico_mensagens = data['historico']
    chat_novo = data['chat_novo']
    data_envio = data['data_envio']
    mensagem = data['mensagem']

    # Verifica a necessidade de criar um chat novo
    if chat_novo:
        try:
            chat_id = registrar_chat(usuario_id,materia_id,"Teste")
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

    #realizar busca semantica e gerar resposta com mcp aqui
    model = "ollama3"
    materia = "Matemática"
    socketio.start_background_task(_mcp_background_task, materia_id, mensagem, historico_formatado, sid, model, materia)

def _mcp_background_task(materia_id, mensagem, historico, sid, model, materia):
    try:
        import asyncio

        coro = call_tool_local(
            "chat",
            {
                "materia_id": materia_id,
                "mensagem": mensagem,
                "historico": historico,
                "sid": sid,
                "model": model,
                "materia": materia
            }
        )

        def runner():
            try:
                asyncio.run(coro)
            except Exception as e:
                socketio.emit("llm_error", {"erro": str(e)}, to=sid)

        t = Thread(target=runner, daemon=True)
        t.start()

    except Exception as e:
        socketio.emit("llm_error", {"erro": str(e)}, to=sid)
