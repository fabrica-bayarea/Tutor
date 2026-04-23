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

                # 🔥 garante erro explícito se API falhar
                if response.status_code != 200:
                    text = await response.aread()
                    raise RuntimeError(
                        f"Ollama error {response.status_code}: {text.decode()}"
                    )

                buffer = ""

                async for chunk in response.aiter_bytes():
                    if not chunk:
                        continue

                    buffer += chunk.decode("utf-8", errors="ignore")

                    # NDJSON = linhas separadas por \n
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()

                        if not line:
                            continue

                        try:
                            data = json.loads(line)
                        except Exception as e:
                            print(f"[Ollama parse warning] {line} | {e}")
                            continue

                        # 🔥 stream de resposta
                        if "response" in data:
                            yield data["response"]

                        # 🔥 finalização segura
                        if data.get("done"):
                            return

                # 🔥 flush final (caso não tenha newline no último chunk)
                if buffer.strip():
                    try:
                        data = json.loads(buffer)
                        if "response" in data:
                            yield data["response"]
                    except Exception as e:
                        print(f"[Ollama final buffer parse error] {e}")