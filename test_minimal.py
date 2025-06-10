#!/usr/bin/env python3
"""
Minimal test to isolate the hanging issue
"""
import asyncio
from huggingface_hub.inference._mcp.agent import Agent

async def minimal_test():
    print("🔧 Minimal MCP test")
    
    # Create agent
    agent = Agent(
        model="local-model",
        base_url="http://localhost:1234/v1", 
        api_key="lm-studio",
        servers=[{
            "type": "stdio",
            "config": {
                "command": "node",
                "args": ["mcp-servers/src/filesystem/dist/index.js", "test-recipes"]
            }
        }],
        prompt="You are a test agent."
    )
    
    print("✅ Agent created")
    
    # Load tools
    print("Loading tools...")
    await agent.load_tools()
    print("✅ Tools loaded")
    
    # Try ONE simple message
    print("Sending message...")
    response_parts = []
    async for chunk in agent.run("Just say hello, don't use any tools."):
        if hasattr(chunk, 'content') and chunk.content:
            response_parts.append(chunk.content)
        print(".", end="", flush=True)  # Show progress
        
    response = ''.join(response_parts)
    print(f"\n✅ Response: {response}")

if __name__ == "__main__":
    asyncio.run(minimal_test())