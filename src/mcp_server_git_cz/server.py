import os
import anyio
import click
import mcp.types as types
from mcp.server.lowlevel import Server
from dotenv import load_dotenv

from .tool.commit_message_tool import CommitMessageTool

load_dotenv()


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    app = Server("mcp-git-commit-generator")
    llm_provider = os.environ.get("LLM_PROVIDER", "deepseek")
    commit_message_tool = CommitMessageTool(llm_provider)

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        if name != "generate_commit_message":
            raise ValueError(f"Unknown tool: {name}")
        
        content_blocks = []
        async for content in commit_message_tool.call(name, arguments):
            content_blocks.append(content)
        
        # Combine the streamed content into a single TextContent block
        full_text = "".join(
            [block.text for block in content_blocks 
             if isinstance(block, types.TextContent)]
        )
        return [types.TextContent(type="text", text=full_text)]

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="generate_commit_message",
                title="Commit Message Generator",
                description=(
                    "Generate a commit message from the git changes "
                    "in the current project directory."
                ),
                inputSchema={"type": "object", "properties": {}},
            )
        ]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.responses import Response
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )
            return Response()

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse, methods=["GET"]),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="127.0.0.1", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0