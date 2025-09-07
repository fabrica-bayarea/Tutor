# Tutor

Guia de configuração para o ambiente de desenvolvimento e produção do projeto.

## Stack de Tecnologias

- **Frontend:** JavaScript com [Next.js](https://nextjs.org/) e React.
- **Backend:** Python com [Flask](https://flask.palletsprojects.com/) e [Gunicorn](https://gunicorn.org/) para produção.
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/).
- **LLM:** Integração com modelos de linguagem via [Ollama](https://ollama.com/).
- **Ambiente:** Totalmente containerizado com [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/).

## Como Rodar o Projeto

O ambiente é 100% containerizado com Docker, simplificando a configuração para desenvolvimento e produção.

### Pré-requisitos

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/download)

_Nota: Atualmente, o serviço da LLM (Ollama) precisa ser executado na máquina local. Após instalar o Ollama, baixe o modelo `mistral` que o projeto utiliza com o seguinte comando:_

```bash
ollama pull mistral
```

### Configuração e Execução

1.  **Clone o Repositório:**

    ```bash
    git clone https://github.com/fabrica-bayarea/Tutor.git
    cd Tutor
    ```

2.  **Crie o Arquivo de Ambiente Principal (`./.env`):**

    - Na **raiz do projeto**, crie um arquivo chamado `.env`.
    - Adicione a senha que será usada pelo banco de dados:

    ```
    # Arquivo: ./.env
    POSTGRES_PASSWORD=sua_senha_segura_aqui
    ```

3.  **Crie o Arquivo de Ambiente do Backend (`./backend/.env`):**

    - Dentro da pasta `backend/`, crie outro arquivo chamado `.env`.
    - **IMPORTANTE:** O `POSTGRES_PASSWORD` deve ser o mesmo que você definiu no passo anterior.

    ```
    # Arquivo: ./backend/.env
    SECRET_KEY=gere_uma_chave_secreta_aqui
    DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/tutor
    DB_HOST=db
    # Opcional para desenvolvimento backend:
    FLASK_DEBUG=1
    ```

### Executando os Ambientes

Com o Docker Desktop e o Ollama em execução, você pode iniciar os containers.

#### Ambiente de Desenvolvimento
Ideal para codificar, pois possui **hot-reload** (as alterações no código são aplicadas automaticamente).

```bash
# Na raiz do projeto, execute:
docker-compose up --build
```
#### Ambiente de Produção
Simula o ambiente real de produção, usando o servidor Gunicorn (backend) e o build otimizado do Next.js. Não possui hot-reload.

```bash
# Na raiz do projeto, execute:
docker-compose -f docker-compose.prod.yml up --build
```

### Acessando a Aplicação

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend API:** [http://localhost:5000](http://localhost:5000)

### Parando a Aplicação

- Para parar todos os containers, pressione `Ctrl + C` no terminal.
- Para remover os containers (mas manter os dados do banco), use `docker-compose down` (adicione -f docker-compose.prod.yml se estiver no ambiente de produção).
