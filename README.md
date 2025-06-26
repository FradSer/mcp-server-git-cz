# Git Commit Message Generator MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

> An intelligent MCP server that automatically generates [Conventional Commits](https://www.conventionalcommits.org/) style commit messages using LLM providers like DeepSeek and Groq.

## Features

- **AI-Powered**: Leverages LLM providers (DeepSeek, Groq) for intelligent commit message generation
- **Conventional Commits**: Follows industry-standard commit message conventions
- **Multi-Provider**: Supports multiple LLM providers with easy switching
- **MCP Compatible**: Works seamlessly with Claude, Cursor, Gemini CLI, and other MCP clients
- **Easy Setup**: Simple configuration via environment variables

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [MCP Client Setup](#mcp-client-setup)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Quick Start

1. **Clone and install**:
   ```bash
   git clone https://github.com/example/mcp-server-git-cz.git
   cd mcp-server-git-cz
   uv venv && uv pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the server**:
   ```bash
   uv run mcp-server-git-cz
   ```

## Installation

### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) package manager

### Step-by-step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/example/mcp-server-git-cz.git
   cd mcp-server-git-cz
   ```

2. **Create virtual environment and install dependencies**:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file:
   ```env
   DEEPSEEK_API_KEY=your_deepseek_api_key
   GROQ_API_KEY=your_groq_api_key
   LLM_PROVIDER=deepseek  # or groq
   ```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek API key | - | Yes (if using DeepSeek) |
| `GROQ_API_KEY` | Groq API key | - | Yes (if using Groq) |
| `LLM_PROVIDER` | LLM provider to use | `deepseek` | No |

### Transport Options

The server supports multiple transport methods:

```bash
# STDIO transport (recommended)
uv run mcp-server-git-cz

# SSE transport
uv run mcp-server-git-cz --transport sse --port 8000
```

## Usage

The server exposes a single tool: `generate_commit_message` that analyzes your git diff and generates conventional commit messages.

### Basic Example

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
            
            # Generate commit message
            result = await session.call_tool("generate_commit_message", {})
            print(result)

asyncio.run(main())
```

## MCP Client Setup

> **Note**: Replace `/path/to/mcp-server-git-cz` with your actual project directory path in all configurations below.

### Claude Code

```bash
# Project scope (recommended for teams)
claude mcp add git-cz -s project -- uv run --python /path/to/mcp-server-git-cz/.venv/bin/python -m mcp_server_git_cz

# User scope (personal use)
claude mcp add git-cz -s user -- uv run --python /path/to/mcp-server-git-cz/.venv/bin/python -m mcp_server_git_cz
```

### Cursor

Add to Cursor settings:

```json
{
  "mcpServers": {
    "git-cz": {
      "command": "uv",
      "args": ["run", "--python", "/path/to/mcp-server-git-cz/.venv/bin/python", "-m", "mcp_server_git_cz"],
      "env": {},
      "transport": "stdio"
    }
  }
}
```

### Gemini CLI

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "git-cz": {
      "command": "uv",
      "args": ["run", "--python", "/path/to/mcp-server-git-cz/.venv/bin/python", "-m", "mcp_server_git_cz"],
      "env": {}
    }
  }
}
```

<details>
<summary>Detailed Setup Instructions</summary>

### Finding Your Paths

1. **Get virtual environment path**:
   ```bash
   cd mcp-server-git-cz
   uv venv
   which python  # Copy this path
   ```

2. **Get project directory**:
   ```bash
   pwd  # Copy this path
   ```

3. **Update configurations** with your actual paths

### Advanced Configuration

#### With Environment Variables
```json
{
  "mcpServers": {
    "git-cz": {
      "command": "uv",
      "args": ["run", "--python", "/path/to/mcp-server-git-cz/.venv/bin/python", "-m", "mcp_server_git_cz"],
      "env": {
        "DEEPSEEK_API_KEY": "your_key_here",
        "LLM_PROVIDER": "deepseek"
      }
    }
  }
}
```

#### With Working Directory
```json
{
  "mcpServers": {
    "git-cz": {
      "command": "uv",
      "args": ["run", "--python", "/path/to/mcp-server-git-cz/.venv/bin/python", "-m", "mcp_server_git_cz"],
      "cwd": "/path/to/mcp-server-git-cz",
      "env": {}
    }
  }
}
```

</details>

## Examples

### Using with MCP Clients

Once configured, you can interact with the tool using natural language:

- *"Generate a commit message for my current changes"*
- *"Create a conventional commit message based on my git diff"*
- *"Help me write a commit message following conventional commits"*

The server will:
1. Analyze your current git diff
2. Generate a conventional commit message using AI
3. Return the formatted message for review

### Example Output

```
feat(auth): add OAuth2 integration with GitHub

- Implement OAuth2 authentication flow
- Add GitHub provider configuration
- Update user model to support external auth
- Add tests for authentication endpoints

Closes #123
```

## Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `make test`
5. Commit using conventional commits: `git commit -m 'feat: add amazing feature'`
6. Push to your branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code
- Use [Black](https://black.readthedocs.io/) for code formatting
- Add type hints where appropriate
- Write tests for new features

### Reporting Issues

Found a bug? Have a feature request? Please [open an issue](https://github.com/example/mcp-server-git-cz/issues) with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [Full documentation](https://github.com/example/mcp-server-git-cz/wiki)
- **Bug Reports**: [GitHub Issues](https://github.com/example/mcp-server-git-cz/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/example/mcp-server-git-cz/discussions)
- **Email**: support@example.com

## Acknowledgments

- [Conventional Commits](https://www.conventionalcommits.org/) specification
- [Model Context Protocol](https://modelcontextprotocol.io/) framework
- [DeepSeek](https://www.deepseek.com/) and [Groq](https://groq.com/) for AI capabilities
- All [contributors](https://github.com/example/mcp-server-git-cz/contributors) who help improve this project

---

<div align="center">
  <strong>Made with ❤️ for the developer community</strong>
  <br>
  <sub>⭐ Star this repo if you find it useful!</sub>
</div>