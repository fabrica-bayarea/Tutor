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
  
    
### Passo 1: Configuração Inicial

1.  **Clone o Repositório:**
    ```
    git clone https://github.com/fabrica-bayarea/Tutor.git
    cd Tutor
    ```
2.  Crie os Arquivos de Ambiente (.env):

    Você precisará de dois arquivos de configuração. A senha do PostgreSQL deve ser a mesma em todos eles.

    - **Arquivo do Backend (`./backend/.env`):** Usado pelo Flask e docker compose.

      ```
      SECRET_KEY=gere_uma_chave_secreta_aqui
      POSTGRES_PASSWORD=sua_senha_segura_aqui
      DATABASE_URL=postgresql://seu_usuario_postgres:sua_senha_segura_aqui@postgres-service:5432/tutor
      DB_HOST=postgres-service
      FLASK_DEBUG=1
      GOOGLE_CLIENT_ID=id do cliente para login com google
      ```

    - **Arquivo do Frontend (`./frontend/.env.local`):** Usado pelo Next.js.
    
      ```
      NEXT_PUBLIC_API_URL_RUNTIME=http://localhost:5000
      NEXT_PUBLIC_GOOGLE_CLIENT_ID=id do cliente para login com google
      ```

### Passo 2: Configurando a LLM

1.  Crie a imagem do Ollama:
    
```
cd ollama
docker build -t seu-usuario/ollama-mistral:latest .
```

2.  Inicie o servidor Ollama e teste localmente:
    
```
docker run -p 11434:11434 seu-usuario/ollama-mistral:latest
curl http://localhost:11434/api/generate -d '{"model":"mistral","prompt":"Olá, mundo!"}'
```

3.  Teste a conexão:

```
ollama run mistral "Olá, mundo!"
```

4.  Suba a imagem para o DockerHub:

```
#realize o login no terminal
docker login

#faça o push da imagem para o seu repositório remoto docker
docker push seu-usuario/ollama-mistral:latest
```

### Passo 3: Construindo a Imagem Docker Universal

Este é o passo mais importante. Construa a imagem do backend e a imagem flexível do frontend que será usada em ambos os ambientes.

```
# Backend
cd backend
docker build -t tutor-backend:latest -f Dockerfile.prod .
cd ..

# Frontend
cd frontend
docker build -t tutor-frontend:flexible .
cd ..

```

### Passo 4: Subindo imagens para o DockerHub

```
#faça o push das imagens para o seu repositório remoto docker
docker push seu-usuario/tutor-backend:latest
docker push seu-usuario/tutor-frontend:flexible
```

### Passo 5: Executando a Aplicação Kubernetes (Simulando Deploy de Produção)

Este método faz o deploy da aplicação em um cluster Kubernetes local, neste tutorial estará sendo utilizado o kubernetes imbutido no docker desktop pela sua facilidade de configuração.

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
#delete qualquer segredo anterior para evitar erros
kubectl delete secret postgres-secret

#crie o novo segredo
kubectl create secret generic postgres-secret --from-env-file=backend/.env
```
    
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
    
### Passo 6: Configurando o Ingress

O ingress é responsável por alterar a url de acesso à aplicação.

1.  Altere o host/paths listado no arquivo /k8s/ingress.yaml da forma que preferir, ele será sua nova url de acesso

2.  Instalar o NGINX Ingress Controller:

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

Após a instalação, confira se os pods foram subidos:

``` 
kubectl get pods -n ingress-nginx
```

Você deve ver algo como ingress-nginx-controller em estado Running

3.  Valide os serviços

O ingress aponta para dois Services, backend-service na porta 5000 e frontend-service na porta 80, verifique se eles existem e estão corretos:

```
kubectl get svc
```

4.  Aplique o ingress:

```
kubectl apply -f k8s/ingress.yaml
```

5. Configure o host local:

Abra o bloco de notas como administrador e entre no diretório C:\Windows\System32\drivers\etc\hosts, abra o arquivo hosts e adicione esta linha ao final dele:

```
127.0.0.1 tutor.local
```

---

### Acessando a Aplicação

- **Ambiente Kubernetes:**

  - Frontend: Acesse via [http://tutor.local/](http://tutor.local/)
  - Backend API: [http://tutor.local/api](http://tutor.local/api) (O serviço `Ingress` expõe a API diretamente nesta porta para acesso externo).

### Parando a Aplicação

- **Docker Compose:** Pressione `Ctrl + C` no terminal e depois `docker compose down`.
- **Kubernetes:** Execute `kubectl delete -f k8s/`.
