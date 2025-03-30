"""
SSH execution MCP server entry point.
"""
from .server import mcp, load_configuration

# Load configuration at module initialization time
load_configuration()

# Export the FastMCP instance for use by the entry point
__all__ = ["mcp"]
