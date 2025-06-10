#!/usr/bin/env python3
"""
Test just agent creation and simple run (no MCP)
"""
import asyncio
from huggingface_hub.inference._mcp.agent import Agent

async def test_simple_only():
    print("🔧 Testing agent without MCP...")
    
    try:
        # Create agent without any MCP servers
        agent = Agent(
            model="local-model",
            base_url="http://localhost:1234/v1",
            api_key="lm-studio",
            servers=[],  # No MCP servers
            prompt="You are a test agent."
        )
        print("✅ Agent created")
        
        print("Testing simple run...")
        response_parts = []
        
        async for chunk in agent.run("Say hello"):
            if hasattr(chunk, 'content') and chunk.content:
                response_parts.append(chunk.content)
                
        response = ''.join(response_parts)
        print(f"✅ Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple_only())