"""
Geração de respostas via AWS Bedrock (substituindo Ollama).

Usa o modelo configurado na variável BEDROCK_MODEL_ID (padrão: Claude 3 Haiku).
O streaming é feito via invoke_model_with_response_stream do Bedrock Runtime.
"""
import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    return _client


async def consultar_llm(prompt: str, modelo: str = None) -> str:
    """
    Faz uma requisição ao AWS Bedrock em modo stream,
    emite chunk a chunk e retorna a resposta completa ao final.

    Args:
        prompt: O prompt a ser enviado ao modelo.
        modelo: Ignorado (mantido por compatibilidade). Usa BEDROCK_MODEL_ID.

    Yields:
        Chunks de texto da resposta.
    """
    client = _get_client()
    model_id = modelo if modelo and modelo.startswith("anthropic.") else BEDROCK_MODEL_ID

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    })

    response = client.invoke_model_with_response_stream(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    for event in response["body"]:
        chunk_data = json.loads(event["chunk"]["bytes"])

        if chunk_data.get("type") == "content_block_delta":
            texto = chunk_data.get("delta", {}).get("text", "")
            if texto:
                yield texto

        elif chunk_data.get("type") == "message_stop":
            break
