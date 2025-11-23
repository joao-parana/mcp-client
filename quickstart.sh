#!/bin/bash
# Quick Start Script for MCP Client with Ollama

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     MCP Client - Quick Start Setup (Ollama + MacBook M3)  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Step 1: Check Python version
echo -e "${YELLOW}[1/6] Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.13"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 13) else 1)" 2>/dev/null; then
    echo -e "${RED}❌ Python 3.13+ required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}\n"

# Step 2: Install dependencies
echo -e "${YELLOW}[2/6] Installing Python dependencies...${NC}"
if command -v uv &> /dev/null; then
    echo "Using uv..."
    uv sync
else
    echo "Using pip..."
    pip install -e .
fi
echo -e "${GREEN}✅ Dependencies installed${NC}\n"

# Step 3: Check if Ollama is installed
echo -e "${YELLOW}[3/6] Checking Ollama installation...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama not found${NC}"
    echo ""
    echo "Please install Ollama:"
    echo "  - Visit: https://ollama.ai"
    echo "  - Or run: brew install ollama"
    echo ""
    exit 1
fi
echo -e "${GREEN}✅ Ollama is installed${NC}\n"

# Step 4: Check if Ollama is running
echo -e "${YELLOW}[4/6] Checking Ollama server...${NC}"
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Ollama server not running${NC}"
    echo "Starting Ollama server..."
    ollama serve &
    sleep 2
fi
echo -e "${GREEN}✅ Ollama server is running${NC}\n"

# Step 5: Check for recommended model
echo -e "${YELLOW}[5/6] Checking for recommended model (qwen2.5:7b)...${NC}"
if ! ollama list | grep -q "qwen2.5:7b"; then
    echo -e "${YELLOW}⚠️  Model not found. Downloading qwen2.5:7b...${NC}"
    echo "This may take a few minutes (4.7GB download)..."
    ollama pull qwen2.5:7b
else
    echo -e "${GREEN}✅ Model qwen2.5:7b is available${NC}"
fi
echo ""

# Display available models
echo -e "${BLUE}Available Ollama models:${NC}"
ollama list
echo ""

# Step 6: Test the client
echo -e "${YELLOW}[6/6] Testing MCP Client...${NC}"
if [ -f "examples/mcp_server/mcp_server.py" ]; then
    echo "Testing list members command..."
    python3 -m mcp_client examples/mcp_server/mcp_server.py --members
    echo -e "${GREEN}✅ MCP Client is working!${NC}\n"
else
    echo -e "${YELLOW}⚠️  Test server not found at examples/mcp_server/mcp_server.py${NC}\n"
fi

# Success message
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    🎉 Setup Complete! 🎉                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

echo -e "${BLUE}Next Steps:${NC}\n"

echo -e "${GREEN}1. Start chatting with Ollama:${NC}"
echo "   python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama"
echo ""

echo -e "${GREEN}2. Try different models:${NC}"
echo "   # Fast and lightweight"
echo "   python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama --model llama3.2:3b"
echo ""
echo "   # Ultra-fast tiny model"
echo "   python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama --model llama3.2:1b"
echo ""
echo "   # Highest quality (slower)"
echo "   python3 -m mcp_client examples/mcp_server/mcp_server.py --chat --provider ollama --model phi4:14b"
echo ""

echo -e "${GREEN}3. List server capabilities:${NC}"
echo "   python3 -m mcp_client examples/mcp_server/mcp_server.py --members"
echo ""

echo -e "${BLUE}Recommended models for MacBook M3:${NC}"
echo "  • qwen2.5:7b   - Best overall balance (DEFAULT)"
echo "  • llama3.2:3b  - Fast and efficient"
echo "  • llama3.2:1b  - Ultra lightweight"
echo "  • phi4:14b     - Highest quality"
echo ""

echo -e "${BLUE}Pull additional models:${NC}"
echo "  ollama pull llama3.2:3b"
echo "  ollama pull phi4:14b"
echo ""

echo -e "${BLUE}Documentation:${NC}"
echo "  • README.md - Full documentation"
echo "  • MIGRATION.md - Migration guide"
echo "  • USAGE_EXAMPLES.sh - Usage examples"
echo "  • .env.example - Environment configuration"
echo ""

echo -e "${BLUE}Troubleshooting:${NC}"
echo "  • Check Ollama: curl http://localhost:11434/api/tags"
echo "  • List models: ollama list"
echo "  • Start server: ollama serve"
echo ""
