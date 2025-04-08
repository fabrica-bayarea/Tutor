# Tutor/backend

## IMPORTANTE
Para conseguir executar corretamente o backend da aplicação, você deve, **no mínimo**:
* Utilizar uma versão do **Python** entre **3.8** e **3.11**
    * Sugerimos utilizar a _major version_ **3.11**. Qualquer _minor version_ (3.11.0, 3.11.9, etc) deve funcionar bem
* Ter o **PostgreSQL** instalado no seu computador
    * Utilizamos a versão **[17.4](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)**
    * [Veja este vídeo curto](https://youtu.be/UbX-2Xud1JA?si=AyfZm32b7bheRwxS) para guiá-lo na instalação
* Ter o **database** do PostgreSQL devidamente criado, assim como suas **tabelas**
    * Consulte o líder da equipe de backend para mais informações

**Algumas dependências do backend _exigem_ que você utilize um gerenciador de pacotes do seu sistema operacional. Consulte a seção **[Dependências do backend](#dependências-do-backend)** para mais informações.**

## Instalação
Supondo que você já tenha clonado o repositório, **certifique-se de que você está na pasta `backend`**, e então:

1. Crie seu ambiente virtual:
    ```bash
    python -m venv venv
    ```
    Ou, se quiser garantir que ele seja criado com uma versão específica (como a **3.11**):
    * No **Windows**:
        ```bash
        py -3.11 -m venv venv
        ```
    * No **Linux/MacOS**:
        ```bash
        python3.11 -m venv venv
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

    _Se a instalação do **ChromaDB** apresentar problemas, consulte a solução mais abaixo na seção **[Dependências do backend](#dependências-do-backend)**._

4. Crie um arquivo `.env` também na pasta `backend` e configure as variáveis de ambiente necessárias:
    ```bash
    DATABASE_URL=url_do_postgresql
    ```

    _Consulte o líder da equipe de backend para auxiliá-lo na configuração do arquivo `.env`._

5. Aplique as migrações do banco de dados PostgreSQL:
    ```bash
    flask db upgrade
    ```

## Estrutura do backend do projeto
Estamos usando uma **arquitetura modular baseada em camadas**, onde cada camada tem um propósito específico.

```
tutor/
└── backend/
    ├── application/
    │   ├── config/         # Define configurações globais da aplicação (bancos de dados, variáveis de ambiente, etc)
    │   ├── libs/           # Contém códigos de bibliotecas auxiliares
    │   ├── models/         # Define as entidades do banco de dados PostgreSQL
    │   ├── routes/         # Define os endpoints da API Flask
    │   ├── services/       # Contém regras de negócio, operações complexas e interações com os bancos de dados
    │   ├── utils/          # Contém funções genéricas que podem ser usadas em todo o projeto, como tratamento de datas, etc
    ├── data/               # Dados locais do ChromaDB e outros arquivos persistentes
    ├── migrations/         # Arquivos de controle de migração do Flask-Migrate
    ├── tests/              # Testes unitários e de integração
    ├── .env                # Arquivo de variáveis de ambiente
    ├── app.py              # Inicialização da aplicação Flask
    ├── README.md           # Documentação do projeto
    └── requirements.txt    # Arquivo de dependências do backend
```

**Por questões de segurança, o arquivo `.env` e a pasta `data` não são (e nem devem) ser enviados para o repositório.**

## Dependências do backend
### python-dotenv
python-dotenv é uma biblioteca que permite carregar variáveis de ambiente de um arquivo `.env`.

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
        * Provavelmente ao selecionar a primeira opção (**C++ CMake Tools for Windows**) o **MSVC v143** já será selecionado automaticamente, facilitando a busca

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

### openai-whisper
Whisper é uma biblioteca da OpenAI que permite transcrever áudio em texto.

### ffmpeg
FFmpeg é um software de codificação de áudio e vídeo, usada para extrair áudio de vídeos. **Ele é necessário para que o Whisper funcione corretamente.**
> Diferentemente das outras dependências, o FFmpeg não é uma biblioteca instalada pelo **gerenciador de pacotes do Python (`pip`)**. Ele é um software de linha de comando que precisa estar instalado **no seu sistema** através de algum **gerenciador de pacotes _de sistema_** para funcionar corretamente. Para isso, siga os passos abaixo:

1. Instale um **gerenciador de pacotes de sistema** no seu computador:
    * Para **Windows**:
        * A melhor opção é o [Chocolatey](https://chocolatey.org/install)
    * Para **MacOS**:
        * A melhor opção é o [Brew](https://brew.sh/)

2. Instale o FFmpeg no seu computador utilizando o gerenciador de pacotes de sistema:
    * No **Windows**:
        * Abra o prompt de comando **como administrador** e execute:
            ```bash
            choco install ffmpeg
            ```
    * No **Linux/MacOS**:
        * Abra o terminal e execute:
            ```bash
            brew install ffmpeg
            ```

### selenium
Ferramenta para automação de navegadores, usada para testes e interação com páginas web.

### webdriver-manager
Facilita o uso do Selenium, baixando e configurando automaticamente os drivers dos navegadores.
