import asyncio
from flask_socketio import emit
from flask import request, current_app

from application.socket.Impl.registrar_chat import registrar_chat
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.socket.Impl.validacao_emit import validacao_emit
from application.socket.Impl.disparar_emit import disparar_emit
from application.mcp.server import executar_chat
from application.socket.socket_instance import socketio
from application.mcp.tools.busca_semantica_tool import busca_semantica
from application.mcp.tools.chat_tool import handle_chat_stream

@socketio.on("connect")
def handle_connect():
    emit("connection-confirmation", {"data": "Conexão estabelecida"})

@socketio.on('mensagem_inicial')
def maestro(data):
    sid = request.sid
    socketio.start_background_task(
        processar_mensagem,
        data,
        sid,
        current_app._get_current_object()
    )

def processar_mensagem(data, sid, app):
    with app.app_context():
        asyncio.run(_processar_mensagem_async(data, sid))

async def _processar_mensagem_async(data, sid):
    disparar_emit(socketio, 'processando', {}, sid)

    try:
        validacao_emit(data)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)

    usuario_id = data['id_usuario']
    materia_id = data['materia_id']
    mensagem = data['mensagem']
    historico_mensagens = data.get('historico')
    chat_novo = data['chat_novo']
    chat_id = data['id_chat']
    data_envio = data['data_envio']

    if chat_novo:
        try:
            chat_id = registrar_chat(usuario_id, materia_id, f"{usuario_id}-ChatTeste")
        except Exception as e:
            traceback.print_exc()
            return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)

    try:
        registrar_mensagem(chat_id, usuario_id, None, data_envio, mensagem)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)

    historico_formatado = (
        "\n".join(f"{m['sender']}: {m['content']}" for m in historico_mensagens)
        if historico_mensagens else ""
    )

    model = "llama3"
    materia = "Matemática"

    try:
        await executar_chat(
            {
                "materia_id": materia_id,
                "mensagem": mensagem,
                "historico": historico_formatado,
                "sid": sid,
                "model": model,
                "materia": materia
            }
        )
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)