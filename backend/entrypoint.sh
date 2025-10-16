#!/bin/sh

# O script irá parar imediatamente se um comando falhar
set -e

# Exporta a variável de ambiente para que o Flask a reconheça
export DATABASE_URL=${DATABASE_URL}

# Espera o banco de dados (serviço 'db') estar pronto para aceitar conexões
# Usamos as variáveis de ambiente que o Flask utiliza para saber onde conectar
echo "Aguardando o banco de dados..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "Banco de dados conectado!"

# Aplica as migrações do banco de dados
echo "Aplicando as migrações do banco de dados..."
flask db upgrade
echo "Migrações aplicadas com sucesso."

# Executa o comando principal do container (o que vem depois do ENTRYPOINT no Dockerfile)
# O "$@" pega o comando definido no CMD do Dockerfile
exec "$@"