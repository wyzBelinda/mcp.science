# TXYZ Search MCP Server
A Model Context Protocol (MCP) server for TXYZ Search API. Provides tools for academic and scholarly search, general web search, and smart search(automatically selects the best search type based on the query), user should register a TXYZ API key from [TXYZ Platform](https://platform.txyz.ai/console) before usage.

### Available Tools
- `search_scholar_tool`: Academic and scholarly search
- `search_web_tool`:  General web search functionality
- `search_smart_tool`: Automatically selects the best search type based on the query
Each with arguments:
- `query`: The search query
- `max_results`: The maximum number of results to return

## Installation
### Using uv (recommanded)
When using `uv`, no specific installation is needed. We will use `uvx` to directly run `mcp-txyz-search`.

## Configuration
using uv(after publish done)
```json
{
  "mcpServers": {
    "mcp-txyz-search": {
      "command": "uvx",
      "args": [
        "mcp-txyz-search"
      ],
      "env": {
        "TXYZ_API_KEY": "YOUR_TXYZ_API_KEY_HERE"
      }
    }
  }
}
```
## Environment Variables
The TXYZ Search API provides enhanced search capabilities including web and scholarly searches.

**Configuration Steps:**
You can get API key from [TXYZ Platform](https://platform.txyz.ai/console)
