from flask import Blueprint, request, Response, stream_with_context
import requests
import json

rag_bp = Blueprint("rag", __name__)

@rag_bp.route("/perguntar", methods=["POST"])
def perguntar():
    """
    Endpoint para gerar uma resposta em tempo real usando o modelo Mistral via Ollama.

    Método:
        POST

    URL:
        /rag/perguntar

    Requisição:
        JSON no corpo da requisição com o seguinte formato:
        {
            "pergunta": "Texto da pergunta"
        }

    Retorno:
        Resposta em streaming (text/plain) contendo a resposta do modelo token por token.

    Status HTTP:
        200 - Sucesso
        400 - Campo 'pergunta' ausente

    Exemplo de uso com curl:
        curl -X POST http://localhost:5000/rag/perguntar \
        -H "Content-Type: application/json" \
        -d '{"pergunta": "O que é aprendizado de máquina?"}'
    """

    data = request.json
    pergunta = data.get("pergunta", "")

    if not pergunta:
        return {"erro": "Campo 'pergunta' obrigatório"}, 400

    # Payload enviado para a API local do Ollama
    payload = {
        "model": "mistral",
        "messages": [{"role": "user", "content": pergunta}],
        "stream": True
    }

    def generate():
        """
        Gera tokens em tempo real usando a API local do Ollama.

        Utiliza `stream=True` para receber os dados de forma contínua,
        retornando os fragmentos conforme o modelo vai respondendo.
        """
        with requests.post("http://localhost:11434/api/chat", json=payload, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded = json.loads(line.decode("utf-8"))
                    content = decoded.get("message", {}).get("content", "")
                    yield content

    # Retorna a resposta de forma contínua usando streaming do Flask
    return Response(stream_with_context(generate()), content_type="text/plain")
