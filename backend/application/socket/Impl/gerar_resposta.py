"""
Geração de respostas via AWS Bedrock com Meta Llama 3.

Usa o modelo configurado na variável BEDROCK_MODEL_ID (padrão: Llama 3 8B Instruct).
O streaming é feito via invoke_model_with_response_stream do Bedrock Runtime.
"""
import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "meta.llama3-8b-instruct-v1:0")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    return _client


def _build_llama_prompt(prompt: str) -> str:
    """Formata o prompt no template de chat do Llama 3."""
    return (
        "<|begin_of_text|>"
        "<|start_header_id|>system<|end_header_id|>\n"
        "Você é um tutor educacional do IESB. Responda de forma clara, "
        "objetiva e didática em português brasileiro.<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n"
        f"{prompt}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n"
    )


async def consultar_llm(prompt: str, modelo: str = None) -> str:
    """
    Faz uma requisição ao AWS Bedrock em modo stream,
    emite chunk a chunk e retorna a resposta completa ao final.

    Args:
        prompt: O prompt a ser enviado ao modelo.
        modelo: Model ID opcional. Usa BEDROCK_MODEL_ID se não informado.

    Yields:
        Chunks de texto da resposta.
    """
    client = _get_client()
    # Só usa o modelo passado se for um ID Bedrock válido (contém ".")
    model_id = modelo if modelo and "." in modelo else BEDROCK_MODEL_ID

    body = json.dumps({
        "prompt": _build_llama_prompt(prompt),
        "max_gen_len": 4096,
        "temperature": 0.7,
        "top_p": 0.9,
    })

    response = client.invoke_model_with_response_stream(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    for event in response["body"]:
        chunk_data = json.loads(event["chunk"]["bytes"])

        texto = chunk_data.get("generation", "")
        if texto:
            yield texto

        if chunk_data.get("stop_reason") is not None:
            break
