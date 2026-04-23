from application.mcp.tools.chat_tool import handle_chat_stream
from application.mcp.llm.ollama_client import OllamaClient
from application.mcp.pipeline.rag_pipeline import RAGPipeline
from application.socket.socket_instance import socketio

ollama = OllamaClient()
pipeline = RAGPipeline(ollama)


async def executar_chat(arguments: dict):
    return await handle_chat_stream(arguments, pipeline, socketio)