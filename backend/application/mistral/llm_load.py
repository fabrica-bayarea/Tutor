import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class LLWrapper:
    def __init__(self, modelo_llm: str = "mistralai/Mistral-7B-v0.1"):
        """
        Inicializa o wrapper do modelo de linguagem.

        Espera receber:
        - `modelo_llm`: str - o nome ou caminho do modelo LLM para carregar.

        Prepara o tokenizador e o modelo para inferência no dispositivo disponível (GPU ou CPU).
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(modelo_llm)
        self.modelo_llm = AutoModelForCausalLM.from_pretrained(
            modelo_llm,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )

    def generate(self, prompt: str, max_length: int = 512) -> str:
        """
        Gera texto a partir do prompt fornecido.

        Espera receber:
        - `prompt`: str - o texto de entrada para o modelo gerar a continuação.
        - `max_length`: int - o número máximo de tokens a serem gerados (padrão 512).

        Retorna o texto gerado pelo modelo.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.modelo_llm.generate(
            **inputs,
            max_new_tokens=max_length,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
