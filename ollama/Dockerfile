# Base oficial do Ollama
FROM ollama/ollama:latest

# Baixa o modelo Mistral durante o build
RUN ollama pull mistral

# Expõe a porta padrão do Ollama
EXPOSE 11434

# Comando padrão para iniciar o servidor Ollama
CMD ["ollama", "serve"]
