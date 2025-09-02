# Tutor / Backend

Este documento descreve como configurar e rodar o ambiente de desenvolvimento do backend do projeto Tutor utilizando Docker.

## Rodando o Projeto com Docker

A maneira recomendada para rodar o ambiente completo é utilizando o Docker Compose a partir da **raiz do projeto**. Isso garantirá que o backend, o frontend e o banco de dados sejam iniciados e conectados corretamente.

### Pré-requisitos
* [Git](https://git-scm.com/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Passos para a Configuração

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/fabrica-bayarea/Tutor.git](https://github.com/fabrica-bayarea/Tutor.git)
    cd Tutor
    ```

2.  **Crie o Arquivo de Ambiente Principal:**
    * Na raiz do projeto, crie um arquivo chamado `.env`.
    * Adicione a senha do banco de dados a ele. Esta senha será usada pelo container do PostgreSQL.
    ```
    # Arquivo: ./.env
    POSTGRES_PASSWORD=sua_senha_segura_aqui
    ```

3.  **Crie o Arquivo de Ambiente do Backend:**
    * Dentro da pasta `backend/`, crie outro arquivo chamado `.env`.
    * Adicione as seguintes variáveis. **IMPORTANTE:** O `POSTGRES_PASSWORD` deve ser o mesmo que você definiu no passo anterior.
    ```
    # Arquivo: ./backend/.env
    SECRET_KEY=gere_uma_chave_secreta_aqui
    DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/tutor
    DB_HOST=db
    # Opcional para desenvolvimento:
    FLASK_DEBUG=1
    ```

4.  **Inicie os Containers:**
    * Com o Docker Desktop rodando, execute o seguinte comando na **raiz do projeto**:
    ```bash
    docker-compose up --build
    ```
    * Na primeira vez, o Docker irá construir as imagens, o que pode levar alguns minutos. O script de inicialização do backend irá aguardar o banco de dados ficar pronto e aplicará as migrações (`flask db upgrade`) automaticamente.

### Acessando a Aplicação
* **Frontend:** [http://localhost:3000](http://localhost:3000)
* **Backend API:** [http://localhost:5000](http://localhost:5000)

### Parando a Aplicação
* Para parar todos os containers, pressione `Ctrl + C` no terminal onde o `docker-compose` está rodando.
* Para remover os containers (mas manter os dados do banco), rode `docker-compose down`.


## Estrutura do back-end do projeto
Estamos usando uma **arquitetura modular baseada em camadas**, onde cada camada tem um propósito específico.
```
Tutor/
└── backend/
├── application/
│   ├── auth/          # Contém códigos de autenticação
│   ├── config/        # Define configurações globais da aplicação
│   ├── libs/          # Contém códigos de bibliotecas auxiliares
│   ├── models/        # Define as entidades do banco de dados PostgreSQL
│   ├── routes/        # Define os endpoints da API Flask
│   ├── services/      # Contém regras de negócio e interações com os bancos
│   ├── socket/        # Configurações do Flask-SocketIO
│   └── utils/         # Contém funções genéricas
├── migrations/      # Arquivos de controle de migração do Flask-Migrate
├── .env             # Arquivo de variáveis de ambiente (local)
├── app.py           # Inicialização da aplicação Flask
├── Dockerfile       # Instruções para construir a imagem Docker do backend
├── entrypoint.sh    # Script de inicialização do container
└── requirements.txt # Arquivo de dependências do backend
```

**Por questões de segurança, os arquivos `.env` não são (e nem devem) ser enviados para o repositório.**