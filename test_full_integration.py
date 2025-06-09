#!/usr/bin/env python3
"""
Test full integration: tiny-agents + LM Studio + MCP
"""
import asyncio
from sage_agent_tiny import SageAgent

async def test_full_integration():
    """Test the complete pipeline with LM Studio running"""
    print("🌿 Testing Full Integration: Tiny-Agents + LM Studio + MCP")
    print("=" * 60)
    
    agent = SageAgent()
    
    try:
        print("🔧 Initializing agent...")
        await agent.initialize()
        print("✅ Agent initialized successfully")
        
        # Test 1: Simple query to verify LM Studio connection
        print("\n📡 Test 1: Basic LM Studio connectivity")
        response1 = await agent.chat("Hello! Can you introduce yourself?")
        print(f"Response: {response1}")
        
        # Test 2: Use MCP tools to list recipes
        print("\n📁 Test 2: List available recipes using MCP tools")
        response2 = await agent.chat("What recipe files are in the test-recipes directory? Please use the available tools to check.")
        print(f"Response: {response2}")
        
        # Test 3: Read and analyze a recipe
        print("\n📖 Test 3: Read and analyze the sample recipe")
        response3 = await agent.chat("Please read the sample-recipe.md file and give me a detailed analysis of the recipe, including ingredients, techniques, and any dietary considerations.")
        print(f"Response: {response3}")
        
        print("\n🎉 Full integration test complete!")
        print("✅ Tiny-agents framework working with LM Studio and MCP servers")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_full_integration())