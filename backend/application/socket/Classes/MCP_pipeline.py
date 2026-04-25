import httpx

class MCPPipeline:

    def __init__(self):
        self.base_url = "http://mcp:9000"
    
    async def run_stream(self, prompt: str, model: str):
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", f"{self.base_url}/stream", json={"prompt": prompt, "model": model}) as response:
                async for chunk in response.aiter_text():
                    yield chunk

    async def valid_stream(self, prompt:str):
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(f"{self.base_url}/validate", json={"prompt": prompt})
            return response.text.strip() == "Válido"