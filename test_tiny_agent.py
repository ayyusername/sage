#!/usr/bin/env python3
"""
Test tiny-agents implementation
"""
import asyncio
from sage_agent_tiny import SageAgent

async def test_tiny_agent():
    """Test the tiny-agents powered Sage agent"""
    print("🔧 Testing Sage Agent with tiny-agents...")
    
    agent = SageAgent()
    
    try:
        # Test initialization
        await agent.initialize()
        print("✅ Agent initialized successfully")
        
        # Test basic functionality (without LM Studio for now)
        print("✅ Agent ready for testing with LM Studio")
        
        # Show available tools info
        print("\n📋 Agent Configuration:")
        print(f"   - Model: {await agent.load_config()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tiny_agent())