"""Entry point for running the HarxitFlow Agentic MCP server.

This allows running the server with:
    python -m harxitflow.agentic.mcp
"""

from harxitflow.agentic.mcp.server import mcp

if __name__ == "__main__":
    mcp.run()
