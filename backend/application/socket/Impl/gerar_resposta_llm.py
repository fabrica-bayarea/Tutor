from application.socket.Impl.disparar_emit import disparar_emit
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from datetime import datetime
from application.mcp.client_manager import MCPClientManager

async def gerar_resposta_llm(prompt_completo, id_llm, socket, id_mensagem, id_chat, sessao_id):
    try:
        if not id_llm:
            print("local", id_llm)
            id_llm = "local"

        room = f"chat_{id_chat}"

        session = MCPClientManager()
        await session.connect_to_server()

        resultado = await session.call_tool(
            "consultar_llm",
            {
                "prompt": prompt_completo[-1]["content"],
                "api_key_id": id_llm
            }
        )

        resposta = ""

        if resultado:
            resposta += resultado[0].text if resultado else ""
        
        disparar_emit(socket, 'mensagem_completa', {
            "id_mensagem": id_mensagem,
            "resposta": resposta
        }, room=room)

        registrar_mensagem(
            id_chat=id_chat,
            usuario_id=None,
            sessao_id=sessao_id,
            data_de_envio=datetime.now(),
            conteudo=resposta
        )

    except Exception as e:
        print("ERRO REAL:", e)
        disparar_emit(socket, 'server_error', {
            "id_mensagem": id_mensagem,
            "error_message": str(e)
        }, room=room)