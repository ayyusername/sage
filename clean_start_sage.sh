#!/bin/bash
echo "🌿 Starting Clean Sage Agent (No Conflicts)"

# Kill any existing MCP processes
pkill -f "mcp-servers"
pkill -f "filesystem"

# Wait a moment
sleep 2

echo "Starting fresh MCP session..."
source test_env/bin/activate
python3 sage_agent_tiny.py