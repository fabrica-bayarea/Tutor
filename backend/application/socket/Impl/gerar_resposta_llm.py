from application.socket.Impl.disparar_emit import disparar_emit
from application.socket.Impl.registrar_mensagem import registrar_mensagem
from application.socket.Impl.llm_providers import obter_provider
from datetime import datetime


def obter_provedor_llm(id_llm):

    if id_llm.startswith("gpt"):
        from openai import AsyncOpenAI
        return AsyncOpenAI()

    elif id_llm.startswith("claude"):
        import anthropic
        return anthropic.AsyncAnthropic()

    elif id_llm.startswith("gemini"):
        import google.generativeai as genai
        return genai

    elif id_llm == "local":
        from app.local_llm import LocalLLMClient
        return LocalLLMClient()

    else:
        raise ValueError(f"LLM não suportada: {id_llm}")

async def gerar_resposta_llm(prompt_completo, id_llm, socket, id_mensagem, id_chat, sessao_id):
    try:
        if not id_llm:
            print("local", id_llm)
            id_llm = "local"

        client = obter_provedor_llm(id_llm)
        llm_provider = obter_provider(id_llm)

        texto_acumulado = ""

        room = f"chat_{id_chat}"

        async for delta in llm_provider(client, prompt_completo, id_llm):
            texto_acumulado += delta

            disparar_emit(socket, 'chunk_mensagem', {
            "id_mensagem": id_mensagem,
            "resposta": delta
        }, room=room)
        
        disparar_emit(socket, 'mensagem_completa', {
            "id_mensagem": id_mensagem,
            "resposta": texto_acumulado
        }, room=room)

        registrar_mensagem(
            id_chat=id_chat,
            usuario_id=None,
            sessao_id=sessao_id,
            data_de_envio=datetime.now(),
            conteudo=texto_acumulado
        )

    except Exception as e:
        print("ERRO REAL:", e)
        disparar_emit(socket, 'server_error', {
            "id_mensagem": id_mensagem,
            "error_message": str(e)
        }, room=room)