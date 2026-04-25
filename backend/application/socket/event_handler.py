import asyncio
import traceback

from flask_socketio import emit
from flask import request, current_app

from application.socket.socket_instance import socketio

from application.socket.Impl.registrar_chat import registrar_chat
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.socket.Impl.validacao_emit import validacao_emit
from application.socket.Impl.disparar_emit import disparar_emit
from application.socket.Impl.busca_semantica import busca_semantica
from application.socket.Impl.prompt_builder import build_prompt

from application.socket.Classes.MCP_pipeline import MCPPipeline

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
    if not chat_novo: chat_id = data['id_chat']
    else: chat_id = None
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

    disparar_emit(socketio, 'buscando_arquivos', {}, sid)
    try:
        contexto_vetorial = await busca_semantica(materia_id,mensagem)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)

    prompt = build_prompt(materia,contexto_vetorial,historico_formatado,mensagem)

    disparar_emit(socketio, 'validando_pergunta', {}, sid)
    try:
        valido = await MCP.valid_stream(prompt)
        if not valido:
            disparar_emit(socketio,"chunk_mensagem",{"data":"A mensagem enviada não pode ser respondida por falta de material ou inconsistência com o tema da matéria."}, room=sid)
            return disparar_emit(socketio,"processo_completo",{"chatId":chat_id}, room=sid)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)

    disparar_emit(socketio, 'gerando_resposta', {}, sid)
    try:
        async for chunk in MCP.run_stream(prompt,model):
            disparar_emit(socketio, 'chunk_mensagem', {"data":chunk}, sid)    
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, sid)

    return disparar_emit(socketio,"processo_completo",{"chatId":chat_id}, room=sid)