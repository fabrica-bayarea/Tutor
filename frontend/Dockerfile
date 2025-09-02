# ================ Estágio de Build ================
# Imagem base do Node.js
FROM node:20-alpine AS build

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando os arquivos de definição de dependências
COPY package.json ./
COPY package-lock.json ./

# Instalando as dependências
RUN npm install

# Copiando o restante da aplicação (frontend) para o container
COPY . .

# Construindo a aplicação
RUN npm run build

# ================ Estágio de Produção ================
# Imagem base do Node.js
FROM node:20-alpine AS production

# Definindo o diretório de trabalho
WORKDIR /app

# Copia os arquivos essenciais para rodar a aplicação
COPY --from=build /app/package.json ./
COPY --from=build /app/next.config.ts ./
COPY --from=build /app/public ./public
COPY --from=build /app/.next ./.next

# Copia a pasta node_modules COMPLETA e já funcional do estágio de build
COPY --from=build /app/node_modules ./node_modules

# Expondo a porta que a aplicação irá rodar (Next.js padrão é 3000)
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["./node_modules/.bin/next", "start"]