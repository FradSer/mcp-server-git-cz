#!/bin/bash
# This script runs the mcp-server-git-cz application from any directory.

# The absolute path to the project directory
PROJECT_DIR="/Users/11161778/.mcp/mcp-server-git-cz"

# Change into the project directory, and if successful, run the server.
cd "$PROJECT_DIR" && uv run mcp-server-git-cz
