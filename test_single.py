#!/usr/bin/env python3
"""
Test single test case
"""
import asyncio
from sage_agent_tiny import SageAgent

async def test_2_only():
    """Test only Test 2: Show me ingredients in Cashew Alfredo"""
    print("🧪 Testing Fix for Test 2")
    print("=" * 50)
    
    agent = SageAgent()
    query = "Show me the ingredients in the Cashew Alfredo recipe"
    
    print(f"Query: {query}")
    print("Expected: Should call read_file and list actual ingredients")
    print("-" * 50)
    
    try:
        response = await agent.chat(query)
        print(f"Response:\n{response}")
        
        # Check for ingredients
        expected_ingredients = ["cashew", "garlic", "nutritional yeast", "lemon", "salt", "pepper"]
        found = [ing for ing in expected_ingredients if ing in response.lower()]
        print(f"\nIngredients found: {found} ({len(found)}/6)")
        
        # Check if read_file was called (look for file reference)
        if "sample-recipe" in response.lower():
            print("✅ References correct file")
        else:
            print("❌ Doesn't reference sample-recipe.md")
            
        if len(found) >= 4:
            print("✅ Found most ingredients")
        else:
            print("❌ Missing most ingredients")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_2_only())