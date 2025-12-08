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

    - **Arquivo do Backend (`./backend/.env.compose`):** Usado pelo Flask e docker compose.

      ```
      SECRET_KEY=gere_uma_chave_secreta_aqui
      POSTGRES_PASSWORD=sua_senha_segura_aqui
      DATABASE_URL=postgresql://postgres:sua_senha_segura_aqui@db:5432/tutor
      DB_HOST=db
      FLASK_DEBUG=1
      GOOGLE_CLIENT_ID=id do cliente para login com google
      ```

    - **Arquivo do Backend (`./backend/.env.k8s`):** Usado pelo kubernetes.

      ```
      SECRET_KEY=gere_uma_chave_secreta_aqui
      POSTGRES_PASSWORD=sua_senha_segura_aqui
      DATABASE_URL=postgresql://postgres:sua_senha_segura_aqui@postgres-service:5432/tutor
      DB_HOST=postgres-service
      FLASK_DEBUG=0
      GOOGLE_CLIENT_ID=id do cliente para login com google
      ```

    - **Arquivo do Frontend (`./frontend/.env.compose.local`):** Usado pelo Next.js.
    
      ```
      NEXT_PUBLIC_API_URL_RUNTIME=http://localhost:5000
      NEXT_PUBLIC_GOOGLE_CLIENT_ID=id do cliente para login com google
      ```
      
    - **Arquivo do Frontend (`./frontend/.env.k8s.local`):** Usado pelo Next.js.
    
      ```
      NEXT_PUBLIC_API_URL_RUNTIME=http://backend-service:5000
      NEXT_PUBLIC_GOOGLE_CLIENT_ID=id do cliente para login com google
      ```

### Passo 2: Construindo a Imagem Docker Universal

Este é o passo mais importante. Construa a imagem do backend e a imagem flexível do frontend que será usada em ambos os ambientes.

```
# Backend
cd backend
docker build -t tutor-backend:latest -f Dockerfile.prod .
cd ..

#caso esteja subindo com kubernetes
cp frontend/.env.k8s.local frontend/.env.local

#caso esteja subindo com docker compose
cp frontend/.env.compose.local frontend/.env.local

# Frontend
cd frontend

docker build -t tutor-frontend:flexible .
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
    cp backend/.env.compose backend/.env
    docker compose up
    ```

_Nota: Garanta que o ollama esteja rodando no computador

#### Método B: Kubernetes (Simulando Deploy de Produção)

Este método faz o deploy da aplicação em um cluster Kubernetes local, neste tutorial estará sendo utilizado o lubernetes imbutido no docker desktop pela sua facilidade de configuração.

1.  Abra o Docker Desktop.

2.  Vá em Settings → Kubernetes.

3.  Marque Enable Kubernetes.

4.  Clique em Apply & Restart.

5.  Teste no terminal:

    ```
    kubectl cluster-info
    kubectl get nodes
    ```
    Se retornar um nó docker-desktop, está funcionando.
    
6.  Crie o Segredo do Banco de Dados (se ainda não existir):

    O segredo armazena a senha do banco de dados de forma segura no cluster.

    ```
    cp backend/.env.k8s backend/.env
    kubectl create secret generic postgres-secret --from-env-file=backend/.env
    ```

    _Nota: Se o segredo já existir, delete-o primeiro com `kubectl delete secret postgres-secret`._

7.  Faça o Deploy da Aplicação(na raiz do projeto):

    Aplique todos os manifestos de configuração contidos na pasta k8s/:

    ```
    kubectl apply -f k8s/
    ```

8.  Force a Atualização (se necessário):

    Se você reconstruir a imagem tutor-frontend:flexible e precisar que o Kubernetes a utilize, force uma reinicialização do deployment:

    ```
    kubectl rollout restart deployment frontend-deployment
    ```

9.  Verifique o Status:

    Aguarde alguns minutos e verifique se todos os pods estão com o status Running:

    ```
    kubectl get pods
    kubectl get svc
    ```

---
### Configurando o Ingress

O ingress é responsável por alterar a url de acesso à aplicação.

1.  Altere o host/paths listado no arquivo /k8s/ingress.yaml da forma que preferir, ele será sua nova url de acesso
    
2.  Aplique o ingress:

    ```
    kubectl apply -f k8s/ingress.yaml
    ```

3. Configure o host local:

    ```
    127.0.0.1 tutor.local
    ```

### Ativando a LLM (Ollama)

1.  Baixe o modelo mistral:
    
    ```
    ollama pull mistral
    ```

2.  Inicie o servidor Ollama:
    
    ```
    ollama serve
    ```

3.  Teste a conexão:

    ```
    ollama run mistral "Olá, mundo!"
    ```
    
### Acessando a Aplicação

- **Ambiente Docker Compose:**

  - Frontend: [http://localhost:3000](http://localhost:3000)
  - Backend API: [http://localhost:5000](http://localhost:5000)

- **Ambiente Kubernetes:**

  - Frontend: Acesse via [http://localhost](http://localhost).
  - Backend API: [http://localhost:30001](http://localhost:30001) (O serviço `NodePort` expõe a API diretamente nesta porta para acesso externo).

- **Ambiente Kubernetes(com Ingress):**

  - Frontend: Acesse via [http://tutor.local/](http://tutor.local/)
  - Backend API: [http://tutor.local/api](http://tutor.local/api) (O serviço `Ingress` expõe a API diretamente nesta porta para acesso externo).

### Parando a Aplicação

- **Docker Compose:** Pressione `Ctrl + C` no terminal e depois `docker compose down`.
- **Kubernetes:** Execute `kubectl delete -f k8s/`.
