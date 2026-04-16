import httpx
import asyncio

class ModelOrchestrator:

    def __init__(self, registry):
        self.registry = registry

    async def wait_until_ready(self):
        await self._wait_ollama()
        await self._pull_models()
        await self._verify_models()

    async def _wait_ollama(self):
        url = "http://ollama-service:11434/api/tags"

        while True:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)

                    if response.status_code == 200:
                        print("Ollama disponível!")
                        return

            except Exception:
                pass

            print("Aguardando ollama...")
            await asyncio.sleep(2)

    async def _pull_models(self):
        for llm_id, config in self.registry._models.items():

            if config["provider"] != "ollama":
                continue

            model_name = config["model_name"]

            print(f"Garantindo modelo: {model_name}")

            async with httpx.AsyncClient(timeout=None) as  client:
                await client.post(
                    "http://ollama-service:11434/api/pull",
                    json={"name": model_name}
                )

    async def _verify_models(self):
        async with httpx.AsyncClient() as client:

            r = await client.get("http://ollama-service:11434/api/tags")
            data = r.json()

            available = {m["name"] for m in data.get("models", [])}

            for llm_id, config in self.registry._models.items():
                model = config["model_name"]

                if model not in available:
                    raise Exception(f"Modelo {model} não carregado no Ollama")

            print("Todos os modelos estão prontos!")
    
