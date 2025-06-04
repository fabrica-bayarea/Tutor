import requests

MISTRAL_API_URL =  "https://api.mistral.ai/v1/chat/completions"
MODEL_NAME = "mistral-7b-instruct"  

def gerar_resposta(prompt: str) -> str:
    """
    Função para carregar o modelo da LLM Mistral 7B
    
    Dentro do payload estão os dados que serão enviados para o Mistral via API:
    1 - model: Modelo da LLM
    2 - prompt: Texto de entrada
    3 - max_tokens: Número máximo de tokens nas respostas geradas
    4 - temperature: controla a criatividade nas respostas para as perguntas feitas
    5 - stop: indicativo de quando parar de gerar texto
    
    Abaixo ele faz uma requisição via HTTP para a API do LM Studio
    
    1 - Envia requisição POST para o endpont da LLM
    2 - Usa o payload como corpo da requisição
    3 - Se for bem sucedido ele retorna uma resposta
    4 - Se não for bem sucido ele retorna uma mensagem de erro
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "stop": ["</s>"] 
    }

    try:
        response = requests.post(MISTRAL_API_URL, json=payload)
        response.raise_for_status()
        resposta = response.json().get("response", "").strip()
        return resposta
    except requests.RequestException as e:
        print(f"Erro ao consultar Mistral: {e}")
        return "Erro ao gerar resposta."