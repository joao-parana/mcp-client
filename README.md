# MCP Client

A minimal client for testing Model Context Protocol (MCP) servers, featuring AI integration with support for both OpenAI and Ollama (local LLMs).

## Features

- **MCP server integration**: Connect to any MCP server
- **Server introspection**: List available tools, prompts, and resources with the `--members` option
- **AI-powered chat**: Interactive chat with AI-powered tool execution using the `--chat` option
- **Dual LLM support**: Use OpenAI API or local Ollama models
- **Auto-detection**: Automatically selects the best available provider

## Installation

1. Clone or download the repository

2. Install dependencies:

```console
# Using pip
pip install -e .

# Or using uv (recommended)
uv sync
```

3. Set up your LLM provider:

### Option A: OpenAI (Cloud)

```console
export OPENAI_API_KEY="your-openai-api-key"
```

### Option B: Ollama (Local - Recommended for MacBook M3)

1. Install Ollama from https://ollama.ai
2. Pull a recommended model:

```console
# Best balance for MacBook M3 (default)
ollama pull qwen2.5:7b

# Other excellent options:
ollama pull llama3.2:3b      # Fast and efficient (3GB RAM)
ollama pull llama3.2:1b      # Ultra lightweight (1GB RAM)
ollama pull phi4:14b         # High quality (8GB RAM)
```

3. Ollama runs automatically at `http://localhost:11434`

## Usage

### List Server Members

Inspect what tools, prompts, and resources are available on an MCP server:

```console
python3 -m mcp_client examples/mcp_server/mcp_server.py --members
```

This command will display:
- Tools and their descriptions
- Prompts and their purposes
- Resources and their types

### Interactive Chat Mode

Start an interactive chat session using the MCP server tools:

```console
# Auto-detect provider (uses Ollama if available, otherwise OpenAI)
python3 -m mcp_client examples/mcp_server/mcp_server.py --chat

# Explicitly use Ollama with default model (qwen2.5:7b)
python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama

# Use a specific Ollama model
python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama --model llama3.2:3b

# Use OpenAI
python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider openai

# Use specific OpenAI model
python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider openai --model gpt-4o
```

Example session:

```console
python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama

Using Ollama with model: qwen2.5:7b

MCP Client's Chat Started!
Type your queries or 'quit' to exit.

You: Greet Pythonista

[Used echo({'message': "Hello, Pythonista! 🐍 How's your coding journey going today?"})]
Assistant: Hello, Pythonista! 🐍 How's your coding journey going today?

You: quit

Goodbye!
```

## Configuration

### Environment Variables

You can configure the client using environment variables:

```bash
# OpenAI configuration
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4o-mini"  # Default model

# Ollama configuration
export OLLAMA_MODEL="qwen2.5:7b"   # Default model
export OLLAMA_BASE_URL="http://localhost:11434"  # Default URL
```

### Provider Selection Logic

The client automatically selects a provider in this order:

1. If `--provider` is specified, use that provider
2. If `OPENAI_API_KEY` is set, use OpenAI
3. Otherwise, use Ollama (local)

## Recommended Models for MacBook M3

Based on your MacBook M3 hardware:

| Model | Size | RAM | Best For |
|-------|------|-----|----------|
| **qwen2.5:7b** | 4.7GB | 8GB | **Best overall balance** (default) |
| llama3.2:3b | 2GB | 4GB | Fast responses, good quality |
| llama3.2:1b | 1GB | 2GB | Ultra-fast, simple tasks |
| phi4:14b | 8GB | 12GB | Highest quality, slower |

## Example MCP Server

The project includes `examples/mcp_server/mcp_server.py`, a minimal MCP server that provides:

- A sample tool that echoes messages
- Sample prompts and resources

Use this server to test the client's functionalities.

## Requirements

- Python >= 3.13
- MCP Python SDK (`mcp>=1.22.0`)
- OpenAI Python SDK (`openai>=2.8.1`) - optional, for OpenAI support
- Ollama Python SDK (`ollama>=0.4.0`) - optional, for local LLM support
- An OpenAI API key (if using OpenAI)
- Ollama installed locally (if using local models)
- An MCP server to connect to

## Architecture

The client uses a modular architecture:

- `BaseQueryHandler`: Abstract base class for LLM providers
- `OpenAIQueryHandler`: OpenAI API implementation
- `OllamaQueryHandler`: Ollama local implementation
- `create_query_handler()`: Factory function with auto-detection

This design makes it easy to add new LLM providers in the future.

## Troubleshooting

### Ollama Connection Issues

If you see connection errors with Ollama:

```console
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### Model Not Found

If a model isn't available locally:

```console
# List available models
ollama list

# Pull the missing model
ollama pull qwen2.5:7b
```

### OpenAI API Key Issues

Ensure your API key is properly set:

```console
# Check if key is set
echo $OPENAI_API_KEY

# Set it if missing
export OPENAI_API_KEY="your-key-here"
```
