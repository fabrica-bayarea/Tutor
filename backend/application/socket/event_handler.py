import asyncio
import traceback

from flask_socketio import emit
from application.services.service_materia import buscar_llm_materia_por_id, buscar_materia_por_id
from application.socket.Impl.gerar_resposta import consultar_ollama
from flask import request, current_app

from application.socket.socket_instance import socketio

from application.socket.Impl.registrar_chat import registrar_chat
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.socket.Impl.validacao_emit import validacao_emit
from application.socket.Impl.disparar_emit import disparar_emit
from application.socket.Impl.busca_semantica import busca_semantica
from application.socket.Impl.prompt_builder import build_prompt

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

    # VALIDAÇÃO DE PAYLOAD
    disparar_emit(socketio, 'processando', {}, room=sid)
    try:
        validacao_emit(data)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, room=sid)

    # CRIAÇÃO DE VARIAVEIS LOCAIS
    usuario_id = data['id_usuario']
    materia_id = data['materia_id']
    mensagem = data['mensagem']
    historico_mensagens = data.get('historico')
    chat_novo = data['chat_novo']
    if not chat_novo: chat_id = data['id_chat']
    else: chat_id = None
    data_envio = data['data_envio']

    # VERIFICANDO SE HÁ CONTEXTO LOCAL PARA GERAÇÃO DA RESPOSTA(FINALIZA O FLUXO CASO NÃO HAJA NENHUM CONTEXTO)
    disparar_emit(socketio, 'buscando_arquivos', {}, room=sid)
    try:
        contexto_vetorial = await busca_semantica(materia_id,mensagem)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, room=sid)
    
    if(contexto_vetorial == ''): 
        resposta_erro = "Não encontrei informações confiáveis ou contexto suficiente para responder à sua pergunta de forma precisa. Isto ocorre quando o material disponibilizado pela base de conhecimento é insuficiente para geração da resposta."
        disparar_emit(socketio,"resposta_finalizada",{"resposta":resposta_erro}, room=sid)
        return disparar_emit(socketio,"processo_completo",{"chatId":chat_id,"resposta_completa":resposta_erro}, room=sid)

    # PERSISTÊNCIA/CRIAÇÃO DO CHAT(CASO HAJA NECESSIDADE)
    if chat_novo:
        try:
            chat_id = registrar_chat(usuario_id, materia_id, f"{usuario_id}-ChatTeste")
        except Exception as e:
            traceback.print_exc()
            return disparar_emit(socketio, "erro", {"erro": str(e)}, room=sid)

    # PERSISTÊNCIA DA MENSAGEM
    try:
        registrar_mensagem(chat_id, usuario_id, 'user', None, data_envio, mensagem)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, room=sid)

    # FORMATAÇÃO DO HISTÓRICO DE MENSAGENS(CASO HAJA ALGUM)
    historico_formatado = (
        "\n".join(f"{m['sender']}: {m['content']}" for m in historico_mensagens)
        if historico_mensagens else ""
    )
    
    # BUSCA PELO MODELO REGISTRADO NA MATÉRIA
    model = buscar_llm_materia_por_id(materia_id)
    if model == None: model = "llama3"

    # BUSCA PELO NOME DA MATÉRIA
    materia_registro = buscar_materia_por_id(materia_id)
    materia = materia_registro["nome"]

    # CRIAÇÃO DO PROMPT
    prompt = build_prompt(materia,contexto_vetorial,historico_formatado,mensagem)

    # ENVIO DA PERGUNTA PARA A LLM
    disparar_emit(socketio, 'gerando_resposta', {}, room=sid)
    resposta_completa = ""
    try:
        async for chunk in consultar_ollama(prompt, model):
            resposta_completa += chunk
            disparar_emit(socketio, 'chunk_resposta', {"chunk": chunk}, room=sid)

        disparar_emit(socketio, 'resposta_finalizada', {"resposta": resposta_completa}, room=sid)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, room=sid)

    # PERSISTÊNCIA DA MENSAGEM DA LLM
    try:
        registrar_mensagem(chat_id, None, 'llm', None, data_envio, resposta_completa)
    except Exception as e:
        traceback.print_exc()
        return disparar_emit(socketio, "erro", {"erro": str(e)}, room=sid)
    
    # FINALIZAÇÃO DO FLUXO
    return disparar_emit(socketio,"processo_completo",{"chatId":chat_id,"resposta_completa":resposta_completa}, room=sid)
