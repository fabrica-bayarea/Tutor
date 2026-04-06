# materia_server.py
from mcp.server import Server

from application.services.service_busca import executar_busca_semantica
from application.repositories.repository_materia import obter_arquivos_por_materia

# Cria o servidor MCP
server = Server("materia-server")

# Define a tool genérica de busca semântica
@server.tool("busca_semantica")
def busca_semantica(query: str, subject_tag: str, args: list):
    """
    Realiza busca semântica nos arquivos vinculados à matéria.
    """
    try:
        arquivos_ids = obter_arquivos_por_materia(id_materia)
        return executar_busca_semantica(mensagem_usuario, arquivos_ids)

    except Exception as e:
        return [{"role": "system", "content": f"Erro na busca semântica: {str(e)}"}]

if __name__ == "__main__":
    server.run()