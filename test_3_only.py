#!/usr/bin/env python3
"""
Test only Test 3: Find vegan pasta recipes
"""
import asyncio
from sage_agent_tiny import SageAgent

async def test_3_only():
    """Test only Test 3: Find me vegan pasta recipes"""
    print("🧪 Testing Fix for Test 3")
    print("=" * 50)
    
    agent = SageAgent()
    query = "Find me vegan pasta recipes"
    
    print(f"Query: {query}")
    print("Expected: Should list directory, read files, find pasta recipes")
    print("-" * 50)
    
    try:
        response = await agent.chat(query)
        print(f"Response:\n{response}")
        
        # Check for pasta recipes
        expected_pasta_files = ["pasta-aglio-e-olio.md"]
        found_files = [f for f in expected_pasta_files if f in response.lower()]
        print(f"\nPasta files found: {found_files}")
        
        # Check if list_directory was called
        if "chickpea-salad" in response.lower():
            print("✅ Called list_directory")
        else:
            print("❌ Didn't call list_directory")
            
        # Check if pasta-specific content was found
        if "pasta" in response.lower():
            print("✅ Response mentions pasta")
        else:
            print("❌ Response doesn't mention pasta")
            
        if len(found_files) >= 1:
            print("✅ Found pasta recipe")
        else:
            print("❌ Missing pasta recipe")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_3_only())