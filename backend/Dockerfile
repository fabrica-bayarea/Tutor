# ================ Estágio de Build ================
FROM python:3.11-slim AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ================ Estágio de Produção ================
FROM python:3.11-slim AS production

# Instala netcat-openbsd (essencial para o script de espera) e libpq5 para o Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
        netcat-openbsd \
        libpq5 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia as dependências e o código do estágio de build
COPY --from=build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY --from=build /app .

# Copia o entrypoint explicitamente para a raiz do WORKDIR
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Use o caminho relativo direto ou absoluto
ENTRYPOINT ["/app/entrypoint.sh"]
# Comando padrão para rodar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]
