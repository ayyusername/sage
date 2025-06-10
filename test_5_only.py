#!/usr/bin/env python3
"""
Test only Test 5: Complex Multi-Criteria Search & Ranking
"""
import asyncio
from sage_agent_tiny import SageAgent

async def test_5_only():
    """Test only Test 5: Complex multi-criteria search with ranking"""
    print("🧪 Testing Test 5: Complex Multi-Criteria Search & Ranking")
    print("=" * 70)
    
    agent = SageAgent()
    query = "I'm having guests over and want to impress them with something sophisticated but not too time-consuming. I have mushrooms, cashews, and nutritional yeast on hand. What are my best options, ranked by impressiveness vs. effort?"
    
    print(f"Query: {query}")
    print("Expected: List directory, read 4-6 files, analyze ingredients/complexity, rank recommendations")
    print("-" * 70)
    
    try:
        response = await agent.chat(query)
        print(f"Response:\n{response}")
        
        # Check for available ingredients analysis
        available_ingredients = ["mushroom", "cashew", "nutritional yeast"]
        found_ingredients = [ing for ing in available_ingredients if ing in response.lower()]
        print(f"\nAvailable ingredients mentioned: {found_ingredients}")
        
        # Check for sophistication/impressiveness analysis  
        impressive_words = ["sophisticated", "impress", "elegant", "advanced", "complex", "gourmet"]
        found_impressive = [w for w in impressive_words if w in response.lower()]
        print(f"Sophistication analysis: {found_impressive}")
        
        # Check for effort/time analysis
        effort_words = ["effort", "time", "easy", "difficult", "quick", "advanced", "simple"]
        found_effort = [w for w in effort_words if w in response.lower()]
        print(f"Effort analysis: {found_effort}")
        
        # Check for specific recipe recommendations
        expected_recipes = ["wellington", "alfredo", "onion", "seitan"]
        found_recipes = [r for r in expected_recipes if r in response.lower()]
        print(f"Expected recipes mentioned: {found_recipes}")
        
        # Check for ranking/ordering
        ranking_words = ["rank", "best", "recommend", "first", "second", "most", "top"]
        found_ranking = [r for r in ranking_words if r in response.lower()]
        print(f"Ranking indicators: {found_ranking}")
        
        # Success criteria
        if len(found_ingredients) >= 2:
            print("✅ Analyzes available ingredients")
        else:
            print("❌ Missing ingredient analysis")
            
        if len(found_impressive) >= 1:
            print("✅ Considers sophistication/impressiveness")
        else:
            print("❌ Missing sophistication analysis")
            
        if len(found_effort) >= 2:
            print("✅ Analyzes effort/complexity")
        else:
            print("❌ Missing effort analysis")
            
        if len(found_recipes) >= 2:
            print("✅ Mentions expected recipes")
        else:
            print("❌ Too few relevant recipes")
            
        if len(found_ranking) >= 2:
            print("✅ Provides ranking/recommendations")
        else:
            print("❌ Lacks clear ranking")
            
        # Check for comprehensive analysis
        if "wellington" in response.lower() and "cashew" in response.lower():
            print("✅ Connects recipes to available ingredients")
        else:
            print("❌ Doesn't connect recipes to ingredients")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_5_only())