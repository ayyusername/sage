#!/usr/bin/env python3
"""
Test the simplified agent with file search queries
"""
import asyncio
from sage_agent_simple import SimpleSageAgent

async def test_simplified_file_search():
    """Test file search with the simplified agent"""
    print("🔍 Testing Simplified Agent File Search")
    print("=" * 50)
    
    agent = SimpleSageAgent()
    
    # Test queries
    test_queries = [
        "What recipe files are available?",
        "Find vegan pasta recipes",
        "Tell me about the sample recipe",
        "What ingredients are in the Cashew Alfredo?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📋 Test {i}: '{query}'")
        print("=" * 30)
        
        try:
            response = agent.process_message(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 Summary: File search capability with simplified agent")

if __name__ == "__main__":
    asyncio.run(test_simplified_file_search())