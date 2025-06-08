# Tutor/backend

## IMPORTANTE
Para conseguir executar corretamente o backend da aplicação, **você precisa, no mínimo**:
* Utilizar uma versão do **Python** entre **3.8** e **3.11**
    * Sugerimos utilizar a _major version_ **3.11**. Qualquer _minor version_ (3.11.0, 3.11.9, etc) deve funcionar bem
* Ter o **PostgreSQL** instalado no seu computador
    * Utilizamos a versão **[17.4](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)**
    * [Assista a este vídeo curto](https://youtu.be/UbX-2Xud1JA?si=AyfZm32b7bheRwxS) para guiá-lo na instalação
* Ter o **database** do PostgreSQL devidamente criado
    * Consulte a seção **[Configuração inicial do PostgreSQL](#configuração-inicial-do-postgresql)** para mais informações
* Ter um **gerenciador de pacotes de sistema operacional** instalado
    * Algumas dependências do backend **EXIGEM** que você utilize um gerenciador de pacotes do seu sistema operacional. Consulte a seção **[Dependências do backend](#dependências-do-backend)** para mais informações

## Configuração inicial do PostgreSQL
Supondo que você já tenha instalado o PostgreSQL corretamente, tendo seguido os passos do vídeo recomendado acima:

1. Abra o **pgAdmin**
2. Na aba **Object Explorer**, expanda os conteúdos de **Servers**
    * Ao fazer isso, você terá que inserir sua senha, definida no momento da instalação do PostgreSQL. **Lembre-se dela**.
3. Clique com o botão direito sobre **Databases** e selecione **Create** > **Database**
4. Crie um novo database chamado `tutor`
    * Basta nomeá-lo e salvar. Não se preocupe com outras configurações ou com criar tabelas por agora.

## Instalação do projeto
Supondo que você já tenha clonado o repositório:

1. Abra um terminal e navegue até a pasta `backend/`

    _É **EXTREMAMENTE** importante que você esteja na pasta `backend/` para realizar as etapas seguintes. Fique atento a isso!_

2. Crie seu ambiente virtual:
    ```bash
    python -m venv venv
    ```
    Ou, se quiser garantir que ele seja criado com uma versão específica do Python (como a **3.11**):
    * No **Windows**:
        ```bash
        py -3.11 -m venv venv
        ```
    * No **Linux/MacOS**:
        ```bash
        python3.11 -m venv venv
        ```

3. Ative o ambiente virtual:
    * No **Windows**:
        ```bash
        ./venv/Scripts/activate
        ```
    * No **Linux/Mac**:
        ```bash
        source ./venv/bin/activate
        ```

Certifique-se de estar com o interpretador **do ambiente virtual** ativado antes de prosseguir com as etapas restantes. Para isso:
* Abra algum arquivo Python deste projeto (como o `app.py`)
* Verifique no canto inferior direito do VS Code o interpretador selecionado (algo como `3.11.9 ('venv': venv)`), e clique nele
* Se o caminho para o interpretador ativo não for algo como `./backend/venv/Scripts/python.exe`, procure por um que seja dessa forma
    * Se não encontrar, procure manualmente pelo arquivo `python.exe` no caminho especificado acima

4. **Com o ambiente virtual ativado**, instale as dependências do backend:
    ```bash
    pip install -r requirements.txt
    ```

    _É esperado que a instalação do **ChromaDB** apresente problemas. Para solucioná-los, consulte a seção **[Dependências do backend](#dependências-do-backend)**._

5. Crie um arquivo `.env` também na pasta `backend/` e configure as variáveis de ambiente necessárias:
    ```bash
    DATABASE_URL=postgresql://<usuario>:<senha>@localhost:<porta>/tutor
    ```
    * Substitua os placeholders pelos valores corretos
        * `<usuario>` é o superusuário definido no momento da instalação do PostgreSQL. Provavelmente `postgres`
        * `<senha>` é a senha que **VOCÊ** definiu no momento da instalação do PostgreSQL
        * `<porta>` é a porta definida no momento da instalação do PostgreSQL. Se você não definiu uma personalizada, provavelmente será `5432`, que é a porta padrão do PostgreSQL

6. **Ainda na pasta `backend/` e com o ambiente virtual ativado**, aplique as migrações do banco de dados PostgreSQL:
    ```bash
    flask db upgrade
    ```
    Se houver problemas com o comando acima, tente fazer com que o Python chame diretamente o módulo Flask:
    ```bash
    python -m flask db upgrade
    ```

    _As migrações fornecem um "controle de versionamento" para bancos de dados, como se fosse um Git dedicado a isso. É por meio delas que criamos, alteramos e excluímos tabelas do banco de dados, e deixamos tudo registrado num histórico._

## Estrutura do backend do projeto
Estamos usando uma **arquitetura modular baseada em camadas**, onde cada camada tem um propósito específico.

```
Tutor/
└── backend/
    ├── application/
    │   ├── config/         # Define configurações globais da aplicação (bancos de dados, variáveis de ambiente, etc)
    │   ├── libs/           # Contém códigos de bibliotecas auxiliares
    │   ├── models/         # Define as entidades do banco de dados PostgreSQL
    │   ├── routes/         # Define os endpoints da API Flask
    │   ├── services/       # Contém regras de negócio, operações complexas e interações com os bancos de dados
    │   ├── socket/         # Contém configurações, eventos e gatilhos do Flask-SocketIO
    │   ├── utils/          # Contém funções genéricas que podem ser usadas em todo o projeto, como tratamento de datas, etc
    │   └── constants.py    # Contém constantes globais do projeto
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

### Flask-CORS
Flask-CORS é uma extensão para Flask que permite que você controle quais origens (domínios) podem acessar sua API.

### Flask-SQLAlchemy
Flask-SQLAlchemy é uma extensão para Flask que fornece uma interface ORM (Object-Relational Mapping) para o SQLAlchemy, um framework de ORM para Python.

### Flask-Migrate
Flask-Migrate é uma extensão para Flask que fornece migrações de banco de dados para o SQLAlchemy.

### Flask-SocketIO
Flask-SocketIO é uma extensão para Flask que fornece suporte para Socket.IO, uma biblioteca que permite comunicação em tempo real entre o cliente e o servidor.

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
        * Provavelmente ao selecionar a primeira opção (**C++ CMake Tools for Windows**) o **MSVC v143** já será selecionado automaticamente

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
FFmpeg é um software de codificação de áudio e vídeo, usado para extrair áudio de vídeos. **Ele é necessário para que o Whisper funcione corretamente.**

_Diferentemente das outras dependências, o FFmpeg não é uma biblioteca instalada pelo **gerenciador de pacotes do Python (`pip`)**. Ele é um software de linha de comando que precisa estar instalado **no seu sistema** através de algum **gerenciador de pacotes de sistema** para funcionar corretamente. Para isso, siga os passos abaixo:_

1. Instale um **gerenciador de pacotes de sistema** no seu computador:
    * Para **Windows**, a melhor opção é o [Chocolatey](https://chocolatey.org/install)
    * Para **MacOS**, a melhor opção é o [Brew](https://brew.sh/)

2. Instale o FFmpeg no seu computador utilizando o gerenciador de pacotes de sistema:
    * No **Windows**:
        * Abra o prompt de comando **como administrador** e execute:
            ```bash
            choco install ffmpeg
            ```
    * No **MacOS**:
        * Abra o terminal e execute:
            ```bash
            brew install ffmpeg
            ```

### selenium
Ferramenta para automação de navegadores, usada para testes e interação com páginas web.

### webdriver-manager
Facilita o uso do Selenium, baixando e configurando automaticamente os drivers dos navegadores.