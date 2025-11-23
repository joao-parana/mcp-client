#!/bin/bash
# Quick Start: Test MCP Client Multi-Server Setup

set -e

echo "=================================================="
echo "MCP Client Multi-Server - Quick Start Test"
echo "=================================================="
echo ""

# Check if in correct directory
if [ ! -f "mcp-servers.sh" ]; then
    echo "❌ Error: Run this from mcp-client directory"
    exit 1
fi

echo "Step 1: Making scripts executable..."
chmod +x mcp-servers.sh test_config.py USAGE_EXAMPLES_V2.sh
echo "✅ Done"
echo ""

echo "Step 2: Testing configuration loader..."
python3 test_config.py
if [ $? -ne 0 ]; then
    echo "❌ Configuration tests failed!"
    exit 1
fi
echo ""

echo "Step 3: Listing available servers..."
python3 -m mcp_client --list-servers
echo ""

echo "=================================================="
echo "Setup Complete! ✅"
echo "=================================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Pull Docker images:"
echo "   ./mcp-servers.sh pull"
echo ""
echo "2. Test a server:"
echo "   python3 -m mcp_client --server fetch --members"
echo ""
echo "3. Start interactive chat:"
echo "   python3 -m mcp_client --server fetch --chat --provider ollama"
echo ""
echo "4. See more examples:"
echo "   ./USAGE_EXAMPLES_V2.sh"
echo ""
echo "For full documentation, see:"
echo "  - README.md"
echo "  - conf/MCP_SERVERS_GUIDE.md"
echo "  - MIGRATION_V2.md"
echo ""
echo "=================================================="
