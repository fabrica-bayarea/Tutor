# Imagem oficial do Python como Base
FROM python:3.11-slim

# Atualiza os pacotes do sistema pra corrigir as vulnerabilidades e limpa o cache
RUN apt-get update && \
    apt-get install -y netcat-traditional && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo de dependências para o container
COPY requirements.txt .

# Instalando as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o restante da aplicação (backend) para o container
COPY . .

# Copia o script de entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expondo a porta 5000 (padrão do Flask)
EXPOSE 5000

# Entrypoint do container
ENTRYPOINT [ "./entrypoint.sh" ]

# Comando para iniciar a aplicação
# Host 0.0.0.0 para a aplicação ser acessível de fora do container
CMD ["python", "app.py"]