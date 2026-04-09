
async def gpt_provider(client, prompt, model):
    response = await client.chat.completions.create(model=model, messages=prompt, stream=True)

    async for chunk in response: 
        delta = chunk.choices[0].delta.content or ""

        if delta:
            yield delta