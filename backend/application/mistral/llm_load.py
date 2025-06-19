class LLMWrapper:
    def __init__(self, model_name: str = "mistral"):
        """
        Inicializa o wrapper do modelo de linguagem usando o Ollama local.
        
        Espera receber:
            - `model_name`: Nome do modelo no Ollama (padrão: "mistral")
        """
        self.model_name = model_name
        
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        """
        Gera texto a partir do prompt fornecido usando o Ollama.

        Espera receber:
            - `prompt`: Texto de entrada para o modelo.
            - `max_tokens`: Número máximo de tokens a serem gerados.
            - `temperature`: Controle de aleatoriedade (0.0 a 1.0).
            
        Retorna o texto gerado pelo modelo.
        """
        try:
            import ollama
            
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'num_predict': max_tokens,
                    'temperature': temperature,
                }
            )
            return response['response']
            
        except ImportError:
            raise ImportError("Ollama não está instalado. Instale com: pip install ollama")
        except Exception as e:
            return f"Erro ao gerar texto: {str(e)}"
