#!/bin/sh

NEXT_STATIC_DIR=$(find /app/.next -type d -name "static")

API_URL=${NEXT_PUBLIC_API_URL_RUNTIME:-http://localhost:5000}
GOOGLE_ID=${NEXT_PUBLIC_GOOGLE_CLIENT_ID:-id_padrao_aqui}

echo "Configurando a URL da API para: $API_URL"

grep -rl '__API_URL_PLACEHOLDER__' $NEXT_STATIC_DIR | xargs -r sed -i "s|__API_URL_PLACEHOLDER__|$API_URL|g"
grep -rl '__GOOGLE_ID_PLACEHOLDER__' $NEXT_STATIC_DIR | xargs -r sed -i "s|__GOOGLE_ID_PLACEHOLDER__|$GOOGLE_ID|g"

exec "$@"