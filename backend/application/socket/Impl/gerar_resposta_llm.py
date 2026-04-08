from application.socket.Impl.disparar_emit import disparar_emit
from application.socket.Impl.registrar_mensagem import registrar_mensagem
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
        room = f"chat_{id_chat}"

        if id_llm:
             client = obter_provedor_llm(id_llm)
        else:
             client = "llm id local"

        texto_acumulado = ""

        if id_llm.startswith("gpt"):
            response = await client.chat.completions.create(
                model=id_llm,
                messages=prompt_completo,
                stream=True
            )

            async for chunk in response:
                delta = chunk.choices[0].delta.content or ""

                if delta:
                    texto_acumulado += delta
                    disparar_emit(socket, 'chunk_mensagem', {
                        "id_mensagem": id_mensagem,
                        "delta": delta
                    }, room=room)


        elif id_llm.startswith("claude"):
            response = await client.messages.create(
                model=id_llm,
                messages=prompt_completo,
                stream=True
            )

            async for chunk in response:
                if chunk.type == "content_block_delta":
                    delta = chunk.delta.text or ""

                    if delta:
                        texto_acumulado += delta
                        disparar_emit(socket, 'chunk_mensagem', {
                            "id_mensagem": id_mensagem,
                            "delta": delta
                        },room=room)


        elif id_llm.startswith("gemini"):
            model = client.GenerativeModel(id_llm)

            response = model.generate_content(
                prompt_completo,
                stream=True
            )

            for chunk in response:
                delta = chunk.text or ""

                if delta:
                    texto_acumulado += delta
                    disparar_emit(socket, 'chunk_mensagem', {
                        "id_mensagem": id_mensagem,
                        "delta": delta
                    }, room=room)

        elif id_llm == "local":
            response = client.stream(prompt_completo)

            async for delta in response:
                if delta:
                    texto_acumulado += delta
                    disparar_emit(socket, 'chunk_mensagem', {
                        "id_mensagem": id_mensagem,
                        "delta": delta
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
        })