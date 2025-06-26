# Gemini Customization

This file can be used to customize Gemini's behavior.

## Project Description

This is an MCP server that automatically generates git commit messages in the style of https://commitizen-tools.github.io/commitizen/. It supports multiple LLM providers (DeepSeek and Groq) for generating commit messages.

## Project-Specific Instructions

*   The primary goal of this project is to generate commit messages that adhere to the Commitizen convention.
*   When creating commit messages, follow the format: `type(scope): subject`.
*   Refer to https://commitizen-tools.github.io/commitizen/ for format details.
*   The LLM provider is configured via the `LLM_PROVIDER` environment variable in an `.env` file. Supported values are `deepseek` (default) and `groq`.
*   Ensure the appropriate API key (`DEEPSEEK_API_KEY` or `GROQ_API_KEY`) is set in the `.env` file for the selected provider.