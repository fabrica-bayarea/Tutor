# materia_server.py
from mcp.server import Server
from mcp.server.tools import Tool
from application.config.vector_database import collection

# Cria o servidor MCP
server = Server("materia-server")

# Define a tool genérica de busca semântica
@server.tool("busca_semantica")
def busca_semantica(query: str, subject_tag: str, args: list):

    contexts = collection.query(
    query_texts=[query],
    n_results=5,
    where={"id": {"$in": args}}
    )
    documentos = "\n\n".join([doc for doc in contexts.get('documents', [[]])[0]])

    return documentos

if __name__ == "__main__":
    server.run()