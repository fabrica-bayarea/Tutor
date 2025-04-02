# Tutor/backend

## Instalação
Supondo que você já tenha clonado o repositório, **certifique-se de que você está na pasta `backend`**, e então:

1. Crie seu ambiente virtual:
```bash
python -m venv venv
```

2. Ative o ambiente virtual:
    * No **Windows**:
    ```bash
    .\venv\Scripts\activate
    ```
    * No **Linux/Mac**:
    ```bash
    source venv/bin/activate
    ```

3. **Com o ambiente virtual ativado**, instale as dependências do backend:
```bash
pip install -r requirements.txt
```

_Se tiver problemas com a instalação do **ChromaDB**, consulte a solução mais abaixo na seção **'Dependências do backend'**._

4. Crie um arquivo `.env` na pasta `backend` e configure as variáveis de ambiente necessárias:
```bash
DATABASE_URL=url_do_postgresql
```

## Estrutura do backend do projeto
Estamos usando uma **arquitetura modular baseada em camadas**, onde cada camada tem um propósito específico.

```
tutor/
└── backend/
    ├── app/
    │   ├── config/          # Define configurações globais da aplicação (bancos de dados, variáveis de ambiente, etc)
    │   ├── models/          # Define as entidades do banco de dados PostgreSQL
    │   ├── services/        # Contém regras de negócio, operações complexas e interações com os bancos de dados
    │   ├── libs/            # Contém códigos de bibliotecas auxiliares
    │   ├── routes/          # Define os endpoints da API Flask
    │   ├── utils/           # Contém funções genéricas que podem ser usadas em todo o projeto, como tratamento de datas, etc
    ├── data/                # Dados locais do ChromaDB e outros arquivos persistentes
    ├── migrations/          # Arquivos de controle de migração do Flask-Migrate
    ├── tests/               # Testes unitários e de integração
    ├── .env                 # Arquivo de variáveis de ambiente
    ├── main.py              # Inicialização da aplicação Flask
    ├── README.md            # Documentação do projeto
    └── requirements.txt     # Arquivo de dependências do backend
```

## Dependências do backend
### python-dotenv
python-dotenv é uma biblioteca que permite carregar variáveis de ambiente de um arquivo .env.

### Flask
Flask é um micro-framework web leve e flexível que permite criar APIs e aplicativos web.

### Flask-SQLAlchemy
Flask-SQLAlchemy é uma extensão para Flask que fornece uma interface ORM (Object-Relational Mapping) para o SQLAlchemy, um framework de ORM para Python.

### Flask-Migrate
Flask-Migrate é uma extensão para Flask que fornece migrações de banco de dados para o SQLAlchemy.

### psycopg2
psycopg2 é um driver de banco de dados para PostgreSQL.

### chromadb
ChromaDB é um banco de dados vetorial open-source projetado para aplicações de IA.

_Se tiver problemas com a instalação do **ChromaDB**, talvez você precise instalar o **Microsoft C++ Build Tools** no seu computador. Para isso, siga os passos abaixo:_

1. Baixe e instale o [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

2. Durante a instalação, selecione as seguintes opções:
    * C++ CMake Tools for Windows
    * Windows 10 SDK
        * _Qualquer versão deve funcionar, mas selecione a mais recente disponível_
    * MSVC v142 ou superior

3. Após instalar, reinicie o terminal e tente novamente instalar o ChromaDB **no ambiente virtual** com:
    ```bash
    pip install chromadb
    ```
    ou
    ```bash
    pip install -r requirements.txt
    ```

### docling
Docling é uma poderosa biblioteca que unifica o processamento de vários tipos de documentos, como PDF, DOCX, PPTX, XLSX, HTML, imagens e mais.
