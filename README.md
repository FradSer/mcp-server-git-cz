A simple MCP server that exposes a git commit message generation tool.

## Usage

Start the server using either stdio (default) or SSE transport:

```bash
# Using stdio transport (default)
uv run mcp-server-git-cz

# Using SSE transport on custom port
uv run mcp-server-git-cz --transport sse --port 8000
```

The server exposes a tool named "generate_commit_message" that accepts no arguments.

## Example

Using the MCP client, you can use the tool like this using the STDIO transport:

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    async with stdio_client(
        StdioServerParameters(command="uv", args=["run", "mcp-server-git-cz"])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(tools)

            # Call the generate_commit_message tool
            result = await session.call_tool("generate_commit_message", {})
            print(result)


asyncio.run(main())

```
