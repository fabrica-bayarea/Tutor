
async def local_provider(client, prompt, model):
    response = client.stream(prompt)

    async for delta in response:
        if delta:
            yield delta