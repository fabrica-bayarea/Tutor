from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

import asyncio

from mcp.tools.chat_tool import get_chat_tool, handle_chat_stream
from mcp.llm.model_registry import ModelRegistry
from mcp.llm.orchestrator import ModelOrchestrator
from mcp.llm.router import ModelRouter
from mcp.llm.ollama_client import OllamaClient
from mcp.pipeline.rag_pipeline import RAGPipeline
from application.socket.socket_instance import socketio

server = Server("multi-llm-server")

registry = ModelRegistry()

registry.register("llama3", {"provider":"ollama", "model_name":"llama3"})

orchestrator = ModelOrchestrator(registry)
router = ModelRouter(registry)
ollama = OllamaClient()
pipeline = RAGPipeline(router,registry,ollama)

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [get_chat_tool()]

@server.call_tool()
async def call_tool(name: str, arguments: dict):

    if name == "chat":
        return await handle_chat_stream(arguments, pipeline, socketio)

    raise ValueError("Tool não encontrada")

async def main():
    await orchestrator.preload_models()

    async with stdio_server() as (read,write):
        await server.run(read,write,server.create_initialization_options())

async def call_tool_local(name: str, arguments: dict):
    return await call_tool(name, arguments)

if __name__ == "__main__":
    asyncio.run(main())