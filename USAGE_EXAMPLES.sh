#!/bin/bash
# Example usage scripts for mcp-client with different LLM providers

# Color output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}MCP Client - Usage Examples${NC}\n"

# Example 1: List server members (no LLM needed)
echo -e "${GREEN}1. List MCP Server Members:${NC}"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --members"
echo ""

# Example 2: Auto-detect provider
echo -e "${GREEN}2. Chat with Auto-detected Provider:${NC}"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --chat"
echo ""

# Example 3: Ollama with default model (qwen2.5:7b)
echo -e "${GREEN}3. Chat using Ollama (default model):${NC}"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama"
echo ""

# Example 4: Ollama with lightweight model
echo -e "${GREEN}4. Chat using Ollama (fast lightweight model):${NC}"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama --model llama3.2:3b"
echo ""

# Example 5: Ollama with tiny model
echo -e "${GREEN}5. Chat using Ollama (ultra-fast tiny model):${NC}"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama --model llama3.2:1b"
echo ""

# Example 6: Ollama with high-quality model
echo -e "${GREEN}6. Chat using Ollama (highest quality):${NC}"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama --model phi4:14b"
echo ""

# Example 7: OpenAI with default model
echo -e "${GREEN}7. Chat using OpenAI (default model):${NC}"
echo "export OPENAI_API_KEY='your-key-here'"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider openai"
echo ""

# Example 8: OpenAI with specific model
echo -e "${GREEN}8. Chat using OpenAI (specific model):${NC}"
echo "export OPENAI_API_KEY='your-key-here'"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider openai --model gpt-4o"
echo ""

# Example 9: Using environment variables
echo -e "${GREEN}9. Chat using Environment Variables:${NC}"
echo "export OLLAMA_MODEL='qwen2.5:7b'"
echo "export OLLAMA_BASE_URL='http://localhost:11434'"
echo "python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama"
echo ""

# Quick test commands
echo -e "${BLUE}Quick Test Commands:${NC}\n"
echo -e "${GREEN}Test Ollama is running:${NC}"
echo "curl http://localhost:11434/api/tags"
echo ""

echo -e "${GREEN}List available Ollama models:${NC}"
echo "ollama list"
echo ""

echo -e "${GREEN}Pull recommended model for MacBook M3:${NC}"
echo "ollama pull qwen2.5:7b"
echo ""

echo -e "${GREEN}Start Ollama server (if not running):${NC}"
echo "ollama serve"
echo ""
