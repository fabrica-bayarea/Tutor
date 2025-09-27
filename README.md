# Tutor

Guia de configuração para os ambientes de desenvolvimento e produção do projeto.

## Stack de Tecnologias

* **Frontend:** JavaScript com [Next.js](https://nextjs.org/) e React.
* **Backend:** Python com [Flask](https://flask.palletsprojects.com/) e [Gunicorn](https://gunicorn.org/) para produção.
* **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/).
* **LLM:** Integração com modelos de linguagem via [Ollama](https://ollama.com/).
* **Ambiente:** Totalmente containerizado com [Docker](https://www.docker.com/).
* **Orquestração:** Deploy em [Kubernetes](https://kubernetes.io/) para simulação de produção.

---

## 🚀 Como Rodar o Projeto

Existem duas maneiras de rodar a aplicação: usando **Docker Compose** para um ambiente de desenvolvimento rápido com hot-reload, ou usando **Kubernetes** para simular um deploy de produção completo.

### Pré-requisitos Gerais

Antes de começar, garanta que você tenha os seguintes softwares instalados:

* [Git](https://git-scm.com/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (com o Kubernetes ativado nas configurações)
* [Ollama](https://ollama.com/download)

*Nota: Atualmente, o serviço da LLM (Ollama) precisa ser executado na máquina local. Após instalar o Ollama, baixe o modelo `mistral` que o projeto utiliza:*
```bash
ollama pull mistral
````

### Configuração Inicial (Comum aos dois ambientes)

1.  **Clone o Repositório:**

    ```bash
    git clone [https://github.com/fabrica-bayarea/Tutor.git](https://github.com/fabrica-bayarea/Tutor.git)
    cd Tutor
    ```

2.  **Crie os Arquivos `.env`:**

      * **Arquivo Principal (`./.env`):** Crie este arquivo na raiz do projeto com a senha do banco de dados.
        ```
        # Arquivo: ./.env
        POSTGRES_PASSWORD=sua_senha_segura_aqui
        ```
      * **Arquivo do Backend (`./backend/.env`):** Crie este arquivo dentro da pasta `backend/`. A senha deve ser a mesma do passo anterior.
        ```
        # Arquivo: ./backend/.env
        SECRET_KEY=gere_uma_chave_secreta_aqui
        DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/tutor
        DB_HOST=db
        FLASK_DEBUG=1
        ```

-----

### Método 1: Docker Compose (Ambiente de Desenvolvimento)

Ideal para codificar, pois possui **hot-reload** (as alterações no código são aplicadas automaticamente).

**Execute o comando:**

```bash
# Na raiz do projeto, execute:
docker-compose up --build
```

-----

### Método 2: Kubernetes (Simulando Deploy de Produção)

Este método faz o deploy da aplicação em um cluster Kubernetes local, da mesma forma que seria feito em um ambiente de produção na nuvem.

**1. Crie o Segredo do Banco de Dados:**
Para evitar expor senhas nos arquivos de configuração, o segredo do banco é criado com o seguinte comando. (Lembre-se de adicionar `postgres-secrets.env` ao seu `.gitignore`\!).

  * Crie um arquivo `postgres-secrets.env` na raiz com o conteúdo: `POSTGRES_PASSWORD=sua_senha_segura_aqui`
  * Execute o comando:
    ```bash
    kubectl create secret generic postgres-secret --from-env-file=postgres-secrets.env
    ```
    *Nota: Se o segredo já existir, você precisará deletá-lo primeiro com `kubectl delete secret postgres-secret`.*

**2. Faça o Deploy da Aplicação:**
Aplique todos os manifestos de configuração contidos na pasta `k8s/`:

```bash
kubectl apply -f k8s/
```

**3. Verifique o Status:**
Aguarde alguns minutos e verifique se todos os pods estão com o status `Running`:

```bash
kubectl get pods
```

-----

### Acessando a Aplicação

  * **Frontend:** [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000) (para Docker Compose) ou [http://localhost](https://www.google.com/search?q=http://localhost) (para Kubernetes).
  * **Backend API:** [http://localhost:5000](https://www.google.com/search?q=http://localhost:5000) (para Docker Compose) ou use `kubectl port-forward service/backend-service 5001:5000` para testar no Kubernetes.

### Parando a Aplicação

  * **Docker Compose:** Pressione `Ctrl + C` no terminal e depois `docker-compose down`.
  * **Kubernetes:** Execute `kubectl delete -f k8s/`.

-----

## Tecnologias Utilizadas

  * **Docker:** É uma plataforma de containerização usada para empacotar a aplicação e suas dependências em "containers". O objetivo é criar um ambiente padronizado e isolado, resolvendo o clássico problema "mas na minha máquina funciona" e simplificando drasticamente a configuração inicial do projeto.

  * **Kubernetes (K8s):** É um orquestrador de containers. Uma vez que temos nossas aplicações em containers Docker, o Kubernetes é responsável por gerenciá-las em escala. Ele automatiza o deploy, o escalonamento (criando mais cópias se a demanda aumentar) e a resiliência (substituindo containers que falham), sendo a ferramenta padrão para rodar aplicações em produção.

  * **Next.js:** É um framework React para construir o frontend da aplicação. Ele foi escolhido por oferecer recursos avançados como Server-Side Rendering (SSR) e otimização de build, que resultam em uma aplicação web mais rápida e com melhor performance para o usuário final.

  * **LLM Mistral (via Ollama):** É o Modelo de Linguagem Grande (Large Language Model) que serve como o "cérebro" do nosso chatbot. Ele é responsável por entender as perguntas dos alunos e gerar respostas coerentes com base nos materiais de estudo. Utilizamos o Ollama para facilitar a execução deste modelo no ambiente de desenvolvimento local.