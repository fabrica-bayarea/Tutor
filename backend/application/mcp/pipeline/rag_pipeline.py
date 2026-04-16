from application.mcp.llm.router import ModelRouter
from application.mcp.llm.ollama_client import OllamaClient
from application.mcp.tools.busca_semantica_tool import busca_semantica
from application.mcp.core.prompt_builder import build_prompt
from application.models import Materia

class RAGPipeline:

    def __init__(self, router, registry, ollama_client):
        self.router = router
        self.registry = registry
        self.ollama = ollama_client

    async def run_stream(self,materia_id:str, pergunta:str,historico:str, socketio, sid):

        contexto = await busca_semantica(materia_id,pergunta)

        model_config = self.router.resolve(materia_id)

        materia = Materia.query.filter_by(id=materia_id).first()
        nome_materia = materia.nome if materia else materia_id

        prompt = build_prompt(nome_materia, contexto, historico, pergunta)

        async for chunk in self.ollama.stream_generate(
            model_config["model_name"],
            prompt
        ):
            socketio.emit("chunk_mensagem", {"data": chunk}, to=sid)

        socketio.emit("processo_completo", {"status": "done"}, to=sid)
