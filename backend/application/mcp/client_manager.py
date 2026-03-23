from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client 
import asyncio

class MCPClientManager:
    def __init__(self):
        self.session = None

    async def connect_to_server(self):
        """Conecta ao único MCP Server."""
        server_params = StdioServerParameters(command="python", args=["materia_server.py"])

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.session = session
                return session

    async def call_tool(self, tool_nome, tool_args):
        """Executa uma ferramenta no MCP Server."""
        if not self.session:
            raise RuntimeError("Nenhuma sessão MCP ativa. Conecte primeiro.")

        try:
            return await asyncio.wait_for(
                self.session.call_tool(tool_nome, arguments=tool_args),
                timeout=5
            )
        except asyncio.TimeoutError:
            return None
