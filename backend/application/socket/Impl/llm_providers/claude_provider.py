
async def claude_provider(client, prompt, model):
    response = await client.messages.create(model=model, messages=prompt, stream=True)

    async for chunk in response:
        if chunk.type == "content_block_delta":
            delta = chunk.delta.text or ""
            if delta:
                yield delta