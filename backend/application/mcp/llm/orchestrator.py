import httpx

class ModelOrchestrator:

    def __init__(self, registry):
        self.registry = registry

    async def preload_models(self):

        for llm_id, config in self.registry._models.items():
            if config["provider"] == "ollama":
                await self._pull_ollama_model(config["model_name"])

    async def _pull_ollama_model(self, model_name:str):
        async with httpx.AsyncClient() as client:
            await client.post(
                "http://localhost:11434/api/pull",
                json={"name": model_name}
            )