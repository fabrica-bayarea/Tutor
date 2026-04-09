
async def gemini_provider(client, prompt, model):
    model_instance = client.GenerativeModel(model)

    response = model_instance.generate_content(prompt, stream=True)

    for chunk in response:
        delta = chunk.text or ""
        if delta: 
            yield delta