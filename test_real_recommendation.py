#!/usr/bin/env python3
"""
Test if the agent can make real recommendations from files
"""
import asyncio
from sage_agent_tiny import SageAgent

async def test_file_search_recommendations():
    """Test if agent actually uses files to make recommendations"""
    print("🧪 Testing File Search Agent Recommendations")
    print("=" * 60)
    
    agent = SageAgent()
    
    # Test queries that require actual file access
    test_queries = [
        "What recipes do I have to choose from?",
        "Find me vegan pasta recipes", 
        "What dessert recipes are available?",
        "Show me recipes with mushrooms",
        "What's the quickest recipe I can make?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: '{query}'")
        print("-" * 40)
        
        try:
            response = await agent.chat(query)
            print(f"📝 Response: {response}")
            
            # Check if response contains actual file names
            recipe_files = [
                "sample-recipe.md", "vegan-donuts.md", "vegan-caramelized-onion-dip.md",
                "vegan-kimchi.md", "vegan-beef-wellington.md", "vegan-chicken-seitan.md", 
                "chickpea-salad.md", "pasta-aglio-e-olio.md", "white-bean-salad.md",
                "italian-broccoli-salad.md"
            ]
            
            found_files = [f for f in recipe_files if any(part in response.lower() for part in f.replace('-', ' ').replace('.md', '').split())]
            
            if found_files:
                print(f"✅ SUCCESS: Found specific recipes: {found_files}")
            else:
                print("❌ FAILURE: Generic response, no specific files mentioned")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    print(f"\n🎯 CONCLUSION: Testing complete!")

if __name__ == "__main__":
    asyncio.run(test_file_search_recommendations())