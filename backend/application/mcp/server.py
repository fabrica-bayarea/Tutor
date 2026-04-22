from mcp.server import Server
from mcp.server.stdio import stdio_server

import asyncio

from application.mcp.tools.chat_tool import handle_chat_stream
from application.mcp.llm.ollama_client import OllamaClient
from application.mcp.pipeline.rag_pipeline import RAGPipeline
from application.socket.socket_instance import socketio

server = Server("multi-llm-server")
ollama = OllamaClient()
pipeline = RAGPipeline(ollama)

@server.call_tool()
async def call_tool(name: str, arguments: dict):

    if name == "chat":
        return await handle_chat_stream(arguments, pipeline, socketio)

    raise ValueError("Tool não encontrada")

async def main():
    async with stdio_server() as (read,write):
        await server.run(read,write,server.create_initialization_options())
        print("Server MCP pronto!")


async def call_tool_local(name: str, arguments: dict):
    return await call_tool(name, arguments)

if __name__ == "__main__":
    asyncio.run(main())
