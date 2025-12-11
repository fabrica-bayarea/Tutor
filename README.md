# Tutor

Guia de configuração para os ambientes de desenvolvimento e produção do projeto.

## Stack de Tecnologias

- **Frontend:** JavaScript com [Next.js](https://nextjs.org/) e React.
- **Backend:** Python com [Flask](https://flask.palletsprojects.com/) e [Gunicorn](https://gunicorn.org/) para produção.
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/).
- **LLM:** Integração com modelos de linguagem via [Ollama](https://ollama.com/).
- **Ambiente:** Totalmente containerizado com [Docker](https://www.docker.com/).
- **Orquestração:** Deploy em [Kubernetes](https://kubernetes.io/) para simulação de produção.

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

    - **Arquivo do Backend (`./backend/.env`):** Usado pelo Flask.

      ```
      SECRET_KEY=gere_uma_chave_secreta_aqui
      POSTGRES_PASSWORD=sua_senha_segura_aqui
      DATABASE_URL=postgresql://postgres:sua_senha_segura_aqui@postgres-service:5432/tutor
      DB_HOST=postgres-service
      FLASK_DEBUG=1
      GOOGLE_CLIENT_ID=id do cliente para login com google
      ```

    - **Arquivo do Frontend (`./frontend/.env.local`):** Usado pelo Next.js.
    
      ```
      NEXT_PUBLIC_API_URL_RUNTIME=http://tutor.local/api
      NEXT_PUBLIC_GOOGLE_CLIENT_ID=id do cliente para login com google
      ```
      
### Passo 2: Logando e configurando os usuários:

1.  Realize login com docker e salve o nome de usuário disponibilizado após autentificação:
```
#realize o login no terminal
docker login
```

2.  Altere o arquivo k8s/backend.yaml na linha 17 para que ele aponte corretamente o seu usuário:

```
#linha 17
        image: seu-usuario/tutor-backend:latest
```

3.  Altere o arquivo k8s/frontend.yaml na linha 17 para que ele aponte corretamente o seu usuário:

```
#linha 17
        image: seu-usuario/tutor-frontend:flexible
```

4.  Altere o arquivo k8s/ollama.yaml na linha 17 para que ele aponte corretamente o seu usuário:

```
#linha 17
        image: seu-usuario/ollama-mistral:latest
```

### Passo 3: Configurando a LLM

1.  Crie a imagem do Ollama:
    
```
docker build -t ollama/ollama:latest
```

2.  Inicie o servidor Ollama:
    
```
docker run 11434:11434 ollama/ollama:latest
```

3.  Crie a imagem do mistral:
    
```
ollama pull mistral
```

4.  Teste localmente:
    
```
#abra outro terminal e teste
curl http://localhost:11434/api/generate -d '{"model":"mistral","prompt":"Olá, mundo!"}'
```

5.  Commitar o container em uma nova imagem:

```
#veja o CONTAINER_ID do que rodou
docker ps -a   

docker commit <CONTAINER_ID> seu-usuario/ollama-mistral:latest

#push para o Docker Hub
docker push seu-usuario/ollama-mistral:latest
```


6.  Apagar a imagem localmente(opcional):

Após realizar a criação e envio da imagem para o DockerHub, com o intuito de evitar consumo de armazenamento desnecessário, você poderá apagar a imagem criada LOCALMENTE
OBS: isso pode ser feito pois a aplicação roda com kubernetes, que utiliza as imagens do dockerhub, uma vez tendo elas lá, as locais não são mais necessárias

 - Entre no docker desktop
 - Vá para conteineres
 - Selecione o conteiner que foi utilizado pelo ollama, apague ele
 - Vá para imagens
 - Selecione as duas imagens criadas neste tutorial, ollama/ollama e seu-usuario/ollama-mistral, apague-as

### Passo 4: Configurando Imagens do frontend e backend

1.  Este é o passo mais importante. Construa a imagem do backend e a imagem flexível do frontend que será usada em ambos os ambientes.

```
# Backend
cd backend
docker build -t seu-usuario/tutor-backend:latest -f Dockerfile.prod .
cd ..

# Frontend
cd frontend
docker build -t seu-usuario/tutor-frontend:flexible .
cd ..

```

2.  Agora suba as imagens criadas para o dockerhub

```
#faça o push das imagens para o seu repositório remoto docker
docker push seu-usuario/tutor-backend:latest
docker push seu-usuario/tutor-frontend:flexible
```

3.  Apagar a imagem localmente(opcional):

Após realizar a criação e envio da imagem para o DockerHub, com o intuito de evitar consumo de armazenamento desnecessário, você poderá apagar a imagem criada LOCALMENTE
OBS: isso pode ser feito pois a aplicação roda com kubernetes, que utiliza as imagens do dockerhub, uma vez tendo elas lá, as locais não são mais necessárias

 - Entre no docker desktop
 - Vá para conteineres
 - Selecione o conteiner que foi utilizado pelo frontend/backend, apague-os
 - Vá para imagens
 - Selecione as duas imagens criadas neste tutorial, seu-usuario/tutor-frontend e seu-usuario/tutor-backend, apague-as


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
kubectl apply -f k8s/database
kubectl apply -f k8s/ollama
kubectl apply -f k8s/backend
kubectl apply -f k8s/frontend
```

8.  Verifique o Status:

Aguarde alguns minutos e verifique se todos os pods estão com o status Running:

```
kubectl get pods
```
    
### Passo 6: Configurando o Ingress

O ingress é responsável por alterar a url de acesso à aplicação.

1.  Instalar o NGINX Ingress Controller:

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

2.  Após a instalação, confira se os pods foram subidos:

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

- **Kubernetes:** Execute `kubectl delete -f k8s/`.
