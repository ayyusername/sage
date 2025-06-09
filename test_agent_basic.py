#!/usr/bin/env python3
"""
Test basic agent functionality without LM Studio
"""
import asyncio
from sage_agent import SageAgent

async def test_agent_setup():
    """Test agent initialization and MCP server startup"""
    
    print("🌿 Testing Sage Agent Setup")
    print("-" * 40)
    
    # Initialize agent
    agent = SageAgent()
    print("✅ Agent initialized")
    
    # Start MCP servers
    print("Starting MCP servers...")
    await agent.start()
    print("✅ MCP servers started")
    
    # Test tool execution directly
    print("Testing tool execution...")
    
    # Mock tool call structure
    mock_tool_call = {
        "function": {
            "name": "list_directory",
            "arguments": '{"path": "test-recipes"}'
        }
    }
    
    result = await agent.execute_tool_call(mock_tool_call)
    print(f"✅ Tool call result: {result}")
    
    # Stop servers
    await agent.stop()
    print("✅ MCP servers stopped")
    
    print("\n🎉 Step 1.1 - MCP Server Setup COMPLETE!")
    print("Next: Implement Sage MCP Server with culinary tools")

if __name__ == "__main__":
    asyncio.run(test_agent_setup())