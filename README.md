# Git Commit Message Generator

An MCP server that automatically generates git commit messages in the style of [Commitizen](https://commitizen-tools.github.io/commitizen/). This server leverages LLM providers like DeepSeek and Groq to generate commit messages based on your git diff.

## Features

-   **Conventional Commits:** Generates commit messages following the Conventional Commits specification.
-   **Multiple LLM Providers:** Supports `deepseek` (default) and `groq` for commit message generation.
-   **Easy Configuration:** Configure the LLM provider and API keys using an `.env` file.

## Getting Started

### Prerequisites

-   Python 3.10+
-   [uv](https://github.com/astral-sh/uv)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/example/mcp-server-git-cz.git
    cd mcp-server-git-cz
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```

3.  **Configure your environment:**

    Copy the example `.env` file:

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file to add your API keys and select your preferred LLM provider:

    ```
    DEEPSEEK_API_KEY=your_deepseek_api_key
    GROQ_API_KEY=your_groq_api_key
    LLM_PROVIDER=deepseek # or groq
    ```

## Usage

Start the server using either stdio (default) or SSE transport:

```bash
# Using stdio transport (default)
uv run mcp-server-git-cz

# Using SSE transport on a custom port
uv run mcp-server-git-cz --transport sse --port 8000
```

The server exposes a tool named `generate_commit_message` that accepts no arguments.

## Example

Using the MCP client, you can use the tool like this with the STDIO transport:

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