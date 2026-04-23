from application.mcp.llm.ollama_client import OllamaClient
from application.mcp.tools.busca_semantica_tool import busca_semantica
from application.mcp.core.prompt_builder import build_prompt
from application.socket.Impl.disparar_emit import disparar_emit

class RAGPipeline:

    def __init__(self, ollama: OllamaClient):
        self.ollama = ollama

    async def run_stream(self,materia_id:str, pergunta:str,historico:str, socketio, sid, model:str, materia: str):

        contexto = await busca_semantica(materia_id,pergunta,sid,socketio)

        disparar_emit(socketio, 'construindo_prompt',{}, room=sid)
        prompt = build_prompt(materia, contexto, historico, pergunta)

        async for chunk in self.ollama.stream_generate(model,prompt):
            disparar_emit(socketio, "chunk_mensagem",{"data": chunk}, room=sid)

        disparar_emit(socketio,"processo_completo",{"status":"done"}, room=sid)
