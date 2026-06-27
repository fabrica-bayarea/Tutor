#!/bin/sh

# O script irÃ¡ parar imediatamente se um comando falhar
set -e

# O Host e a URL vÃªm do seu arquivo .env (via Docker Compose)
# No seu .env: DB_HOST=postgres-service
echo "Aguardando o banco de dados em $DB_HOST:5432..."

# Loop de espera usando o Netcat
while ! nc -z "$DB_HOST" 5432; do
  echo "Banco de dados ($DB_HOST) ainda nÃ£o disponÃ­vel. Aguardando..."
  sleep 2
done

echo "Banco de dados conectado com sucesso!"

# Aplica as migraÃ§Ãµes do Flask-Migrate
echo "Aplicando as migraÃ§Ãµes do banco de dados..."
flask db upgrade
echo "MigraÃ§Ãµes aplicadas com sucesso."

# Executa o comando definido no CMD do Dockerfile (Gunicorn)
echo "Iniciando o servidor..."
exec "$@"
