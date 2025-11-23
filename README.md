# MCP Client

A minimal client for testing Model Context Protocol (MCP) servers, featuring AI integration with support for both OpenAI and Ollama (local LLMs).

## Features

- **MCP server integration**: Connect to any MCP server (Python scripts or Docker containers)
- **Multiple server support**: Configure and use multiple MCP servers via `conf/mcp-servers.json`
- **Docker-based servers**: Official MCP servers via Docker (fetch, filesystem, memory, git, time)
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

## Docker-based MCP Servers (New!)

The client now supports official MCP servers running in Docker containers. These servers are pre-configured in `conf/mcp-servers.json`.

### Quick Setup

1. **Make the management script executable**:
   ```bash
   chmod +x mcp-servers.sh
   ```

2. **Pull Docker images**:
   ```bash
   ./mcp-servers.sh pull
   ```

3. **List available servers**:
   ```bash
   python3 -m mcp_client --list-servers
   ```

### Available Docker Servers

| Server | Description |
|--------|-------------|
| **fetch** | Web content fetching and conversion to Markdown |
| **filesystem** | Secure file operations with sandboxed access |
| **memory** | Knowledge graph-based persistent memory |
| **git** | Git repository operations |
| **time** | Time and timezone utilities |

For detailed documentation, see: [conf/MCP_SERVERS_GUIDE.md](conf/MCP_SERVERS_GUIDE.md)

## Usage

### List Available Servers

Show all configured MCP servers:

```console
python3 -m mcp_client --list-servers
```

### Using Docker-based Servers

Use any configured server by name:

```console
# Fetch server - web content fetching
python3 -m mcp_client --server fetch --chat

# Filesystem server - file operations
python3 -m mcp_client --server filesystem --members

# Memory server - knowledge graph
python3 -m mcp_client --server memory --chat --provider ollama

# Git server - repository operations
python3 -m mcp_client --server git --members

# Time server - timezone utilities
python3 -m mcp_client --server time --chat
```

### Using Custom Python Servers (Legacy Mode)

You can still use Python script servers directly:

```console
# List server capabilities
python3 -m mcp_client examples/mcp_server/mcp_server.py --members

# Start interactive chat
python3 -m mcp_client examples/mcp_server/mcp_server.py --chat
```

### Interactive Chat Mode Options

```console
# Auto-detect provider (uses Ollama if available, otherwise OpenAI)
python3 -m mcp_client --server fetch --chat

# Explicitly use Ollama with default model (qwen2.5:7b)
python3 -m mcp_client --server fetch --chat --provider ollama

# Use a specific Ollama model
python3 -m mcp_client --server fetch --chat --provider ollama --model llama3.2:3b

# Use OpenAI
python3 -m mcp_client --server fetch --chat --provider openai

# Use specific OpenAI model
python3 -m mcp_client --server fetch --chat --provider openai --model gpt-4o

# Enable verbose Docker output (for debugging)
python3 -m mcp_client --server fetch --chat --docker-verbose
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

### Server Configuration File

MCP servers are configured in `conf/mcp-servers.json`. This file includes:

- Server name and description
- Docker image and command
- Environment variables
- Mounted directories (for filesystem/git servers)
- Volume configuration (for memory server)
- Capabilities and tools

To add a new server, edit this file following the existing pattern. See [conf/README.md](conf/README.md) for details.

### Provider Selection Logic

The client automatically selects a provider in this order:

1. If `--provider` is specified, use that provider
2. If `OPENAI_API_KEY` is set, use OpenAI
3. Otherwise, use Ollama (local)

## Docker Management Script

The `mcp-servers.sh` script helps manage Docker-based MCP servers:

```bash
# Pull all official MCP server images
./mcp-servers.sh pull

# Build images locally from source
./mcp-servers.sh build

# List installed images
./mcp-servers.sh list

# Test a specific server
./mcp-servers.sh test fetch

# Show information about servers
./mcp-servers.sh info

# Clean up (remove images and volumes)
./mcp-servers.sh clean

# Show help
./mcp-servers.sh help
```

## Recommended Models for MacBook M3

Based on your MacBook M3 hardware:

| Model | Size | RAM | Best For |
|-------|------|-----|----------|
| **qwen2.5:7b** | 4.7GB | 8GB | **Best overall balance** (default) |
| llama3.2:3b | 2GB | 4GB | Fast responses, good quality |
| llama3.2:1b | 1GB | 2GB | Ultra-fast, simple tasks |
| phi4:14b | 8GB | 12GB | Highest quality, slower |

## Example Session

```console
$ python3 -m mcp_client --server fetch --chat --provider ollama

Using configured server: fetch
Description: Web content fetching and conversion for efficient LLM usage
LLM: Ollama with model: qwen2.5:7b

MCP Client's Chat Started!
Type your queries or 'quit' to exit.

You: Fetch the content from https://example.com

[Used fetch({'url': 'https://example.com', 'max_length': 5000})]
Assistant: I've fetched the content from example.com. The page contains...

You: quit

Goodbye!
```

## Requirements

- Python >= 3.13
- MCP Python SDK (`mcp>=1.22.0`)
- OpenAI Python SDK (`openai>=2.8.1`) - optional, for OpenAI support
- Ollama Python SDK (`ollama>=0.4.0`) - optional, for local LLM support
- Docker >= 20.10.0 - required for Docker-based servers
- An OpenAI API key (if using OpenAI)
- Ollama installed locally (if using local models)

## Architecture

The client uses a modular architecture:

### Core Components

- `MCPClient`: Main client class supporting both Python and Docker servers
- `ServerConfigLoader`: Loads and manages server configurations from JSON
- `BaseQueryHandler`: Abstract base class for LLM providers
- `OpenAIQueryHandler`: OpenAI API implementation
- `OllamaQueryHandler`: Ollama local implementation
- `create_query_handler()`: Factory function with auto-detection

### Server Types

1. **Python Script Servers** (legacy): Direct Python scripts using MCP SDK
2. **Docker Servers** (new): Official MCP servers in Docker containers

This design makes it easy to add new servers and LLM providers.

## Troubleshooting

### Docker Issues

```console
# Check if Docker is running
docker info

# Check if images are available
docker images | grep mcp

# Pull missing images
./mcp-servers.sh pull

# Enable verbose output
python3 -m mcp_client --server fetch --chat --docker-verbose
```

### Ollama Connection Issues

```console
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### Model Not Found

```console
# List available models
ollama list

# Pull the missing model
ollama pull qwen2.5:7b
```

### OpenAI API Key Issues

```console
# Check if key is set
echo $OPENAI_API_KEY

# Set it if missing
export OPENAI_API_KEY="your-key-here"
```

### Server Configuration Issues

```console
# List available servers
python3 -m mcp_client --list-servers

# Check configuration file
cat conf/mcp-servers.json

# Validate JSON syntax
python3 -c "import json; json.load(open('conf/mcp-servers.json'))"
```

## Documentation

- **Main Documentation**: This README
- **Docker Servers Guide**: [conf/MCP_SERVERS_GUIDE.md](conf/MCP_SERVERS_GUIDE.md)
- **Configuration README**: [conf/README.md](conf/README.md)
- **Official MCP Docs**: https://modelcontextprotocol.io
- **MCP Servers Repository**: https://github.com/modelcontextprotocol/servers

## Project Structure

```
mcp-client/
├── conf/
│   ├── mcp-servers.json          # Server configurations
│   ├── MCP_SERVERS_GUIDE.md      # Detailed server documentation
│   └── README.md                  # Configuration quick start
├── examples/
│   └── mcp_server/                # Example Python MCP server
├── src/mcp_client/
│   ├── __init__.py
│   ├── __main__.py                # Entry point
│   ├── cli.py                     # Command-line interface
│   ├── config.py                  # Server configuration loader
│   ├── mcp_client.py              # Main client class
│   ├── handlers.py                # LLM provider handlers
│   └── chat.py                    # Chat interface
├── mcp-servers.sh                 # Docker management script
├── pyproject.toml                 # Project configuration
└── README.md                      # This file
```

## Contributing

Contributions are welcome! Areas for improvement:

- Additional LLM provider support
- More MCP server integrations
- Enhanced error handling
- Performance optimizations
- Documentation improvements

## License

MIT License - see [LICENSE.txt](LICENSE.txt)

## Links

- **Repository**: https://github.com/joao-parana/mcp-client
- **Issues**: https://github.com/joao-parana/mcp-client/issues
- **MCP Protocol**: https://modelcontextprotocol.io
- **Official MCP Servers**: https://github.com/modelcontextprotocol/servers
