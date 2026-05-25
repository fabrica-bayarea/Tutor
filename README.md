# Tutor

Guia de configuração para o ambiente de desenvolvimento do projeto.

## Stack de Tecnologias

- **Frontend:** TypeScript com [Next.js](https://nextjs.org/), React e [Lucide](https://lucide.dev/).
- **Backend:** Python com [Flask](https://flask.palletsprojects.com/), [Selenium](https://www.selenium.dev/) e [Docling](https://github.com/DS4SD/docling).
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/) e [ChromaDB](https://www.trychroma.com/).
- **LLM:** Integração com modelos de linguagem via [Ollama](https://ollama.com/).
- **Ambiente:** Totalmente containerizado com [Docker](https://www.docker.com/).

---

## Pré-requisitos

- **Git**
- **Docker Desktop**

---

## Arquivos de Ambiente

Antes de subir os containers, preencha os arquivos `.env` com base nos arquivos `.env.example` disponíveis em cada diretório:

| Arquivo | Localização |
|---|---|
| `.env` | Raiz do projeto `./` |
| `.env` | Backend `./backend/` |
| `.env` | Frontend `./frontend/` |

---

## Inicialização

1. **Clone o repositório**
   ```bash
   git clone https://github.com/fabrica-bayarea/Tutor.git
   cd Tutor
   ```

2. **Preencha os arquivos de ambiente** conforme descrito na seção acima.

3. **Suba os containers**
   ```bash
   docker compose up -d
   ```

4. **Acesse o sistema** em [http://localhost:3000](http://localhost:3000).

---

## Configuração de Uso

Após inicializar o sistema, siga os passos abaixo para configurá-lo:

### 1. Criar usuário administrador

Acesse o banco de dados por meio de um gerenciador (ex.: DBeaver, pgAdmin) e crie manualmente um usuário admin na tabela de usuários.

### 2. Configurar LLM

- Faça login no sistema e acesse a **página de Admin**.
- Vá até **LLM**, adicione um modelo de sua escolha e aguarde o download.
- Ative o modelo no sistema.

### 3. Cadastrar turmas, matérias, professores e alunos

Na **página de Admin**, utilize as seções correspondentes para adicionar:

- **Turmas**
- **Matérias**
- **Professores**
- **Alunos**

### 4. Realizar associações

As associações entre entidades devem ser feitas manualmente via gerenciador de banco de dados:

- Turma → Aluno
- Matéria → Professor → Turma
- Matéria → Turma
