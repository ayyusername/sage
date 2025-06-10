#!/usr/bin/env python3
"""
Test tiny-agents with very long timeouts for slow LM Studio
"""
import asyncio
import time
from huggingface_hub.inference._mcp.agent import Agent

async def test_agent_with_long_timeout():
    print("🔧 Testing Agent with long timeout for slow LM Studio...")
    
    try:
        # Create agent without MCP first
        agent = Agent(
            model="local-model",
            base_url="http://localhost:1234/v1",
            api_key="lm-studio",
            servers=[],  # No MCP servers for this test
            prompt="You are a helpful assistant."
        )
        print("✅ Agent created")
        
        print("Testing with very short message and long timeout...")
        print("(This may take several minutes if LM Studio is slow)")
        
        start_time = time.time()
        response_parts = []
        
        # Use a VERY long timeout - 10 minutes
        async def collect_response():
            async for chunk in agent.run("Hello"):
                if hasattr(chunk, 'content') and chunk.content:
                    response_parts.append(chunk.content)
                    print(".", end="", flush=True)
                    
        await asyncio.wait_for(collect_response(), timeout=600.0)  # 10 minutes
        
        elapsed = time.time() - start_time
        response = ''.join(response_parts)
        print(f"\n✅ Success after {elapsed:.1f}s!")
        print(f"Response: {response}")
        
        return True
        
    except asyncio.TimeoutError:
        elapsed = time.time() - start_time
        print(f"\n❌ Still timed out after {elapsed:.1f}s")
        return False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Error after {elapsed:.1f}s: {e}")
        return False

async def test_agent_with_mcp_long_timeout():
    print("\n🔧 Testing Agent WITH MCP and long timeout...")
    
    try:
        # Create agent with File System MCP
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
            prompt="You are a helpful assistant with access to filesystem tools."
        )
        print("✅ Agent with MCP created")
        
        # Load tools
        print("Loading MCP tools...")
        await agent.load_tools()
        print("✅ MCP tools loaded")
        
        print("Testing file search with long timeout...")
        print("(This may take several minutes)")
        
        start_time = time.time()
        response_parts = []
        
        # Very long timeout for MCP + slow LM Studio
        async def collect_response():
            async for chunk in agent.run("List the files in the current directory using your available tools"):
                if hasattr(chunk, 'content') and chunk.content:
                    response_parts.append(chunk.content)
                    print(".", end="", flush=True)
                    
        await asyncio.wait_for(collect_response(), timeout=600.0)  # 10 minutes
        
        elapsed = time.time() - start_time
        response = ''.join(response_parts)
        print(f"\n✅ MCP Success after {elapsed:.1f}s!")
        print(f"Response: {response}")
        
        return True
        
    except asyncio.TimeoutError:
        elapsed = time.time() - start_time
        print(f"\n❌ MCP still timed out after {elapsed:.1f}s")
        return False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ MCP error after {elapsed:.1f}s: {e}")
        return False

async def main():
    print("🌿 TESTING TINY-AGENTS WITH LONG TIMEOUTS")
    print("=" * 50)
    print("Note: This may take up to 10 minutes per test if LM Studio is very slow")
    print()
    
    # Test 1: Basic agent without MCP
    basic_works = await test_agent_with_long_timeout()
    
    if basic_works:
        print("\n🎉 Basic agent works! Now testing with MCP...")
        # Test 2: Agent with MCP file system
        mcp_works = await test_agent_with_mcp_long_timeout()
        
        if mcp_works:
            print("\n🎉 COMPLETE SUCCESS! Tiny-agents + MCP + LM Studio working!")
        else:
            print("\n⚠️  Basic agent works, but MCP integration still has issues")
    else:
        print("\n⚠️  Basic agent still doesn't work - may be a deeper issue")
    
    print("\n🎯 Long timeout test complete!")

if __name__ == "__main__":
    asyncio.run(main())