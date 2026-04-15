from mcp.types import Tool, TextContent

def get_chat_tool():
    return Tool(
        name="chat",
        description="Responde perguntas com base na matéria usando IA",
        inputSchema={
            "type": "object",
            "properties": {
                "materia_id": {"type": "string"},
                "mensagem": {"type": "string"},
                "historico": {"type": "string"},
                "sid": {"type": "string"}
            },
            "required": ["materia_id", "mensagem","sid"]
        }
    )

async def handle_chat_stream(arguments, pipeline, socketio):
    materia_id = arguments["materia_id"]
    mensagem = arguments["mensagem"]
    historico = arguments.get("historico", "")
    sid = arguments["sid"]

    await pipeline.run_stream(materia_id, mensagem, historico,socketio, sid)

    return [TextContent(type="text", text="stream iniciado")]