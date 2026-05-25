import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")

async def consultar_ollama(prompt: str, modelo: str) -> str:
    """
    Faz uma requisição ao servidor Ollama em modo stream,
    emite chunk a chunk e retorna a resposta completa ao final.

    Args:
        prompt: O prompt a ser enviado ao modelo.
        modelo: O nome do modelo LLM a ser utilizado.

    Returns:
        A resposta completa gerada pelo modelo.
    """
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": modelo,
        "prompt": prompt,
        "stream": True
    }

    resposta_completa = ""

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for linha in response.aiter_lines():
                if linha:
                    dado = json.loads(linha)
                    chunk = dado.get("response", "")
                    resposta_completa += chunk
                    yield chunk  

                    if dado.get("done", False):
                        break
