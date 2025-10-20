# Tutor

Guia de configuração para os ambientes de desenvolvimento e produção do projeto.

## Stack de Tecnologias

- **Frontend:** JavaScript com [Next.js](https://nextjs.org/) e React.
- **Backend:** Python com [Flask](https://flask.palletsprojects.com/) e [Gunicorn](https://gunicorn.org/) para produção.
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/).
- **LLM:** Integração com modelos de linguagem via [Ollama](https://ollama.com/).
- **Ambiente:** Totalmente containerizado com [Docker](https://www.docker.com/).
- **Orquestração:** Deploy em [Kubernetes](https://kubernetes.io/) para simulação de produção.

## Como Rodar o Projeto

O fluxo de trabalho consiste em três etapas principais:

1.  **Configuração Inicial:** Preparar os arquivos de ambiente.
2.  **Build da Imagem:** Construir a imagem Docker universal do frontend.
3.  **Execução:** Escolher um ambiente para rodar a aplicação (Docker Compose ou Kubernetes).

### Pré-requisitos Gerais

Antes de começar, garanta que você tenha os seguintes softwares instalados:

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (com o Kubernetes ativado nas configurações)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)
- [Ollama](https://ollama.com/download)

_Nota: Atualmente, o serviço da LLM (Ollama) precisa ser executado na máquina local. Após instalar o Ollama, baixe o modelo `mistral` que o projeto utiliza:_

```
ollama pull mistral
```

### Passo 1: Configuração Inicial

1.  **Clone o Repositório:**
    ```
    git clone https://github.com/fabrica-bayarea/Tutor.git
    cd Tutor
    ```
2.  Crie os Arquivos de Ambiente (.env):

    Você precisará de três arquivos de configuração. A senha do PostgreSQL deve ser a mesma em todos eles.

    - **Arquivo Principal (`./.env`):** Usado pelo Docker Compose.

      ```
      # Arquivo: ./.env
      POSTGRES_PASSWORD=sua_senha_segura_aqui
      SECRET_KEY=mesma-senha-do-backend-aqui
      ```

    - **Arquivo do Backend (`./backend/.env`):** Usado pelo Flask.

      ```
      # Arquivo: ./backend/.env
      SECRET_KEY=gere_uma_chave_secreta_aqui
      DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/tutor
      DB_HOST=db
      FLASK_DEBUG=1
      ```

### Passo 2: Construindo a Imagem Docker Universal

Este é o passo mais importante. Construa a imagem flexível do frontend que será usada em ambos os ambientes.

```
# Navegue até a pasta do frontend
cd frontend

# Construa a imagem
docker build -t tutor-frontend:flexible .

# Volte para a raiz do projeto
cd ..
```

### Passo 3: Executando a Aplicação

Com a imagem pronta, escolha como você quer rodar o projeto:

#### Método A: Docker Compose (Ambiente de Desenvolvimento)

Ideal para codificar, pois possui **hot-reload**.

1.  Verifique o docker-compose.yml:

    Garanta que o serviço frontend está configurado para usar a imagem tutor-frontend:flexible.

2.  **Execute o comando:**

    ```
    # Na raiz do projeto, execute:
    docker compose up
    ```

_Nota: Garanta que o ollama esteja rodando no computador

#### Método B: Kubernetes (Simulando Deploy de Produção)

Este método faz o deploy da aplicação em um cluster Kubernetes local.

1.  Crie o Segredo do Banco de Dados (se ainda não existir):

    O segredo armazena a senha do banco de dados de forma segura no cluster.

    ```
    kubectl create secret generic postgres-secret --from-env-file=.env
    ```

    _Nota: Se o segredo já existir, delete-o primeiro com `kubectl delete secret postgres-secret`._

2.  Faça o Deploy da Aplicação:

    Aplique todos os manifestos de configuração contidos na pasta k8s/:

    ```
    kubectl apply -f k8s/
    ```

3.  Force a Atualização (se necessário):

    Se você reconstruir a imagem tutor-frontend:flexible e precisar que o Kubernetes a utilize, force uma reinicialização do deployment:

    ```
    kubectl rollout restart deployment frontend-deployment
    ```

4.  Verifique o Status:

    Aguarde alguns minutos e verifique se todos os pods estão com o status Running:

    ```
    kubectl get pods
    ```

---

### Acessando a Aplicação

- **Ambiente Docker Compose:**

  - Frontend: [http://localhost:3000](http://localhost:3000)
  - Backend API: [http://localhost:5000](http://localhost:5000)

- **Ambiente Kubernetes:**

  - Frontend: Acesse via [http://localhost](http://localhost).
  - Backend API: [http://localhost:30001](https://www.google.com/search?q=http://localhost:30001) (O serviço `NodePort` expõe a API diretamente nesta porta para acesso externo).
  - Alternativa para Debug: Se precisar de um túnel de comunicação direto com o serviço, independentemente de sua exposição, o comando `kubectl port-forward service/backend-service 5001:5000` ainda é uma ferramenta útil.

### Parando a Aplicação

- **Docker Compose:** Pressione `Ctrl + C` no terminal e depois `docker compose down`.
- **Kubernetes:** Execute `kubectl delete -f k8s/`.
