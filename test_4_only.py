#!/usr/bin/env python3
"""
Test only Test 4: Comparative Analysis & Recommendation
"""
import asyncio
from sage_agent_tiny import SageAgent

async def test_4_only():
    """Test only Test 4: Quick lunch with high protein"""
    print("🧪 Testing Test 4: Comparative Analysis & Recommendation")
    print("=" * 60)
    
    agent = SageAgent()
    query = "I want to make something quick for lunch that's high in protein. What do you recommend and why?"
    
    print(f"Query: {query}")
    print("Expected: List directory, read 3+ files, analyze protein/time, recommend with reasoning")
    print("-" * 60)
    
    try:
        response = await agent.chat(query)
        print(f"Response:\n{response}")
        
        # Check for protein sources analysis
        protein_sources = ["chickpea", "seitan", "bean", "nut", "cashew", "protein"]
        found_protein = [p for p in protein_sources if p in response.lower()]
        print(f"\nProtein analysis found: {found_protein}")
        
        # Check for time/speed mentions
        time_indicators = ["quick", "fast", "min", "time", "prep", "easy"]
        found_time = [t for t in time_indicators if t in response.lower()]
        print(f"Time analysis found: {found_time}")
        
        # Check for specific recipe recommendations
        recipe_names = ["chickpea", "broccoli", "salad", "wellington", "seitan"]
        found_recipes = [r for r in recipe_names if r in response.lower()]
        print(f"Specific recipes mentioned: {found_recipes}")
        
        # Check for reasoning/analysis
        reasoning_words = ["because", "since", "high in", "contains", "recommend", "good for"]
        found_reasoning = [r for r in reasoning_words if r in response.lower()]
        print(f"Reasoning indicators: {found_reasoning}")
        
        # Success criteria
        if len(found_protein) >= 2:
            print("✅ Analyzes protein content")
        else:
            print("❌ Missing protein analysis")
            
        if len(found_time) >= 2:
            print("✅ Considers time/speed")
        else:
            print("❌ Missing time analysis")
            
        if len(found_recipes) >= 2:
            print("✅ Mentions specific recipes")
        else:
            print("❌ Too few specific recipes")
            
        if len(found_reasoning) >= 2:
            print("✅ Provides reasoning")
        else:
            print("❌ Lacks reasoning/explanation")
            
        # Check for list_directory call
        if "chickpea-salad" in response.lower() or "[file]" in response.lower():
            print("✅ Called list_directory")
        else:
            print("❌ Didn't call list_directory")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_4_only())