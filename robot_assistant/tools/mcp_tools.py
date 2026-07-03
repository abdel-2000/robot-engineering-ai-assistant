import os

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters

ALLOWED_DIRECTORY = os.path.abspath("workspace")

filesystem_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                ALLOWED_DIRECTORY,
            ],
        )
    )
)
