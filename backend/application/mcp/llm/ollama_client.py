import httpx 
import json
import os

BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

class OllamaClient:

    # Este método lista a llm registrada na matéria selecionada
    async def list_models(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/api/tags")
            data = response.json()
            return [materia["name"] for materia in data.get("models",[])]
        
    # Este método gera uma resposta com a LLM de escolha com stream falso    
    async def generate(self,model:str, prompt:str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/generate",
                json={
                    "model":model,
                    "prompt":prompt,
                    "stream":False
                }
            )
            return response.json().get("response","")
    
    # Este método gera uma resposta com a LLM de escolha com stream verdadeiro
    async def stream_generate(self, model: str, prompt: str):
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True
                }
            ) as response:

                async for line in response.aiter_lines():
                    if not line:
                        continue

                    try:
                        data = json.loads(line)
                    except:
                        continue

                    if "response" in data:
                        yield data["response"]

                    if data.get("done"):
                        break