# materia_server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json

from flask import Flask
from application.config.config import Config
from application.config.database import init_db

from application.services.service_busca import executar_busca_semantica
from application.repositories.repository_materia import obter_arquivos_por_materia

# Inicializa o contexto Flask para o SQLAlchemy funcionar
app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY
init_db(app)

server = Server("materia-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="busca_semantica",
            description="Realiza busca semântica nos arquivos vinculados à matéria.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id_materia": {
                        "type": "string",
                        "description": "ID único da matéria."
                    },
                    "mensagem_usuario": {
                        "type": "string",
                        "description": "Mensagem do usuário para busca semântica."
                    }
                },
                "required": ["id_materia", "mensagem_usuario"]
            }
        ),
        
        Tool(
            name="consultar_llm",
            description="Consulta uma LLM",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string"
                    },
                    "api_key_id": {
                        "type": "string"
                    }
                },
                "required": ["prompt"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "busca_semantica":
        try:
            id_materia = arguments["id_materia"]
            mensagem_usuario = arguments["mensagem_usuario"]

            with app.app_context():
                arquivos_ids = obter_arquivos_por_materia(id_materia)
                resultado = executar_busca_semantica(mensagem_usuario, arquivos_ids)

            return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False))]

        except Exception as e:
            return [TextContent(type="text", text=json.dumps(
                [{"role": "system", "content": f"Erro na busca semântica: {str(e)}"}],
                ensure_ascii=False
            ))]
    elif name == "consultar_llm":
        try:
            prompt = arguments["prompt"]

            return[TextContent(
                type="text",
                text=f"Resposta mock: {prompt}"
            )]
        
        except Exception as e:
            return[TextContent(
                type="text",
                text=f"Error LLM: {str(e)}"
            )] 
    
async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())