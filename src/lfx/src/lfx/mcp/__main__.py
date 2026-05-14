"""Entry point for the HarxitFlow MCP server.

Usage:
    python -m lfx.mcp
    # or via console script:
    lfx-mcp

Environment variables:
    HARXITFLOW_SERVER_URL: HarxitFlow server URL (default: http://localhost:7860)
    HARXITFLOW_API_KEY: API key for authentication (skips login)
"""

from lfx.mcp.server import mcp


def main():
    mcp.run()


if __name__ == "__main__":
    main()
