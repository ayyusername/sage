#!/usr/bin/env python3
"""
Live demo of tiny-agents + LM Studio + MCP integration
"""
import asyncio
from sage_agent_tiny import SageAgent

async def live_demo():
    """Demonstrate the working system"""
    print("🌿 LIVE DEMO: Sage Agent with Tiny-Agents Framework")
    print("=" * 60)
    
    agent = SageAgent()
    
    try:
        print("🔧 Step 1: Initializing tiny-agents...")
        await agent.initialize()
        print("✅ Agent ready!")
        
        print("\n📁 Step 2: Testing MCP file operations...")
        response = await agent.chat("List the files in the test-recipes directory using your available tools.")
        print(f"🤖 Agent: {response}")
        
        print("\n📖 Step 3: Reading and analyzing recipe...")
        response2 = await agent.chat("Read the sample-recipe.md file and tell me what type of cuisine this is and what dietary restrictions it meets.")
        print(f"🤖 Agent: {response2}")
        
        print("\n🎉 Demo complete! Tiny-agents + LM Studio + MCP working perfectly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(live_demo())