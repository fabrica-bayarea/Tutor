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

Todas as variáveis de ambiente do projeto estão centralizadas em um único arquivo `.env` na raiz. Copie o `.env.example` e preencha os valores:

```bash
cp .env.example .env
```

### Descrição das variáveis

```env
# Segurança
SECRET_KEY=your_secret_key_here          # Chave secreta do Flask (gere uma string aleatória segura)

# Banco de dados
POSTGRES_PASSWORD=change_your_password   # Senha do PostgreSQL
DATABASE_URL=postgresql://postgres:change_your_password@postgres-service:5432/tutor  # Mantenha o formato, troque apenas a senha
DB_HOST=postgres-service                 # Não alterar (nome do container)

# Flask
FLASK_DEBUG=1                            # 1 para desenvolvimento, 0 para produção

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id          # Client ID do Google Cloud Console
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id  # Mesmo valor acima (exposto ao frontend)

# SMTP (envio de e-mails)
SMTP_HOST=smtp.gmail.com                 # Servidor SMTP
SMTP_PORT=587                            # Porta SMTP (não alterar para Gmail)
SMTP_USER=your_email@gmail.com           # E-mail remetente
SMTP_PASSWORD=your_smtp_app_password     # Senha de app do Gmail (não a senha da conta)
SMTP_FROM=your_email@gmail.com           # E-mail exibido como remetente

# URLs
FRONTEND_URL=http://localhost:3000       # URL do frontend (não alterar para dev local)
NEXT_PUBLIC_API_URL_RUNTIME=http://localhost:5000  # URL do backend (não alterar para dev local)
OLLAMA_URL=http://ollama-service:11434   # Não alterar (nome do container)

# Domínio institucional
EMAIL_DOMINIO=@iesb.edu.br               # Domínio aceito para login via Google
```

---

## Inicialização

1. **Clone o repositório**
   ```bash
   git clone https://github.com/fabrica-bayarea/Tutor.git
   cd Tutor
   ```

2. **Preencha o arquivo de ambiente** conforme descrito na seção acima.

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
