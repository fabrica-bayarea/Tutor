# Tutor

Guia de configuração para os ambientes de desenvolvimento e produção do projeto.

## Stack de Tecnologias

- **Frontend:** JavaScript com [Next.js](https://nextjs.org/) e React.
- **Backend:** Python com [Flask](https://flask.palletsprojects.com/) e [Uvicorn](https://uvicorn.dev/) para produção.
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/).
- **LLM:** Integração com modelos de linguagem via [Ollama](https://ollama.com/).
- **Ambiente:** Totalmente containerizado com [Docker](https://www.docker.com/).
- **Orquestração:** Deploy em [Kubernetes](https://kubernetes.io/) para simulação de produção.
- 
### Fluxo de instalação

1. **Download do Docker Desktop**  
   Instale o Docker Desktop no seu sistema.

2. **Clonar o repositório**
   ```bash
   git clone https://github.com/fabrica-bayarea/Tutor.git
   cd Tutor
   ```

3. **Subir os containers**
   ```bash
   docker compose up -d
   ```

4. **Instalar o modelo Ollama**
   - Entre no console do container do Ollama (substitua `ollama-container` pelo nome/ID real do container):
     ```bash
     docker exec -it <ollama-container> /bin/sh
     ```
   - Dentro do container execute:
     ```bash
     ollama pull ollama3
     ```
   - Saia do container.

5. **Pronto para uso**  
   Após o pull do modelo Ollama a aplicação estará pronta para uso.

---

## Pré requisitos

- **Git**  
- **Docker Desktop** (recomendado com Kubernetes ativado se for usar a parte de orquestração)  
- **kubectl** (se for usar Kubernetes)

---

## Arquivos de ambiente

Crie os arquivos de ambiente conforme necessário:

- **Backend** `backend/.env` (exemplo)
  ```
  SECRET_KEY=gere_uma_chave_secreta_aqui
  POSTGRES_PASSWORD=sua_senha_segura_aqui
  DATABASE_URL=postgresql://postgres:sua_senha_segura_aqui@postgres-service:5432/tutor
  DB_HOST=postgres-service
  FLASK_DEBUG=1
  GOOGLE_CLIENT_ID=id_do_cliente_google
  ```

- **Frontend** `frontend/.env.local` (exemplo)
  ```
  NEXT_PUBLIC_API_URL_RUNTIME=http://tutor.local/api
  NEXT_PUBLIC_GOOGLE_CLIENT_ID=id_do_cliente_google
  ```

- **Raiz** `./.env` (exemplo)
  ```
  SECRET_KEY=gere_uma_chave_secreta_aqui
  POSTGRES_PASSWORD=sua_senha_segura_aqui
  ```

---

## Passos rápidos de build e deploy local

1. Build e subida via Docker Compose
   ```bash
   docker compose up -d --build
   ```

2. Verificar logs e status
   ```bash
   docker compose ps
   docker compose logs -f
   ```

3. Entrar no container Ollama e puxar o modelo
   ```bash
   docker exec -it <ollama-container> /bin/sh
   ollama pull ollama3
   ```
