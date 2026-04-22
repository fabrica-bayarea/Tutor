import httpx 
import json
import os

BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

class OllamaClient:
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
