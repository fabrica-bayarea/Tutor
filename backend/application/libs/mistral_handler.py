from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage, AssistantMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

tokenizer = MistralTokenizer.v3()

def contar_tokens_mensagens(lista_mensagens: list[dict]) -> int:
    """
    Conta o número de tokens de uma sequência de mensagens no formato esperado pela LLM.

    Espera receber:
    - `lista_mensagens`: list[dict] - uma lista de dicionários representando as mensagens
    
    Formato esperado da lista:
    ```json
    [
        {"role": "user", "content": <conteudo>},
        {"role": "assistant", "content": <conteudo>},
        ...
    ]
    ```
    """
    mensagens_formatadas = []

    for m in lista_mensagens:
        if m["role"] == "user":
            mensagens_formatadas.append(UserMessage(content=m["content"]))
        elif m["role"] == "assistant":
            mensagens_formatadas.append(AssistantMessage(content=m["content"]))
        else:
            continue

    request = ChatCompletionRequest(
        messages=mensagens_formatadas,
        model="mistral"
    )

    resultado = tokenizer.encode_chat_completion(request)
    return len(resultado.tokens)
