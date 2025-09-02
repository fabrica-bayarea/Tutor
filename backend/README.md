# Tutor / Backend

Este é o diretório da aplicação backend, construída em Python com o micro-framework Flask.

## Configuração e Execução

A configuração e execução do ambiente completo (Backend, Frontend e Banco de Dados) é gerenciada via Docker Compose.

Por favor, consulte o **[README.md principal na raiz do projeto](../README.md)** para o guia de instalação passo a passo.

## Estrutura do back-end do projeto

Estamos usando uma **arquitetura modular baseada em camadas**, onde cada camada tem um propósito específico.

```
Tutor/
└── backend/
    ├── application/
    │   ├── auth/          # Contém códigos de autenticação
    │   ├── config/        # Define configurações globais da aplicação
    │   ├── libs/          # Contém códigos de bibliotecas auxiliares
    │   ├── models/        # Define as entidades do banco de dados PostgreSQL
    │   ├── routes/        # Define os endpoints da API Flask
    │   ├── services/      # Contém regras de negócio e interações com os bancos
    │   ├── socket/        # Configurações do Flask-SocketIO
    │   └── utils/         # Contém funções genéricas
    ├── migrations/      # Arquivos de controle de migração do Flask-Migrate
    ├── .env             # Arquivo de variáveis de ambiente (local)
    ├── app.py           # Inicialização da aplicação Flask
    ├── Dockerfile       # Instruções para construir a imagem Docker do backend
    ├── entrypoint.sh    # Script de inicialização do container
    └── requirements.txt # Arquivo de dependências do backend
```

**Por questões de segurança, os arquivos `.env` não são (e nem devem) ser enviados para o repositório.**
