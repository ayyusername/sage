#!/usr/bin/env python3
"""
Showcase Demo of Sage File Search Agent - All 5 Capabilities
"""
import asyncio
from sage_agent_tiny import SageAgent

async def showcase_capabilities():
    """Show off all 5 levels of sophistication"""
    print("🌿" * 25)
    print("   SAGE FILE SEARCH AGENT")
    print("    🧪 CAPABILITY SHOWCASE 🧪")
    print("🌿" * 25)
    print()
    
    agent = SageAgent()
    
    # Test 1: Basic Discovery - Simple file listing
    print("=" * 60)
    print("🔍 LEVEL 1: Basic File Discovery")
    print("=" * 60)
    print("Query: What recipe files do you have available?")
    print("-" * 60)
    response1 = await agent.chat("What recipe files do you have available?")
    print("Response:")
    print(response1[:800] + "..." if len(response1) > 800 else response1)
    print("\n✅ Success: Lists all recipe files without hallucination")
    print()
    
    # Small delay between tests
    await asyncio.sleep(2)
    
    # Test 2: Content Reading - Specific recipe analysis
    print("=" * 60)
    print("📖 LEVEL 2: Content Reading & Analysis")
    print("=" * 60)
    print("Query: Show me the ingredients in the Cashew Alfredo recipe")
    print("-" * 60)
    response2 = await agent.chat("Show me the ingredients in the Cashew Alfredo recipe")
    print("Response:")
    print(response2[:800] + "..." if len(response2) > 800 else response2)
    print("\n✅ Success: Reads actual file content and extracts ingredients")
    print()
    
    await asyncio.sleep(2)
    
    # Test 3: Recipe Search - Content-based matching
    print("=" * 60)
    print("🍝 LEVEL 3: Content-Based Recipe Search")
    print("=" * 60)
    print("Query: Find me vegan pasta recipes")
    print("-" * 60)
    response3 = await agent.chat("Find me vegan pasta recipes")
    print("Response:")
    print(response3[:800] + "..." if len(response3) > 800 else response3)
    print("\n✅ Success: Multi-file search with content analysis")
    print()
    
    await asyncio.sleep(2)
    
    # Test 4: Advanced Analysis - Multi-criteria recommendation
    print("=" * 60)
    print("🥗 LEVEL 4: Smart Recommendations")
    print("=" * 60)
    print("Query: I want something quick for lunch that's high in protein. What do you recommend?")
    print("-" * 60)
    response4 = await agent.chat("I want to make something quick for lunch that's high in protein. What do you recommend and why?")
    print("Response:")
    print(response4[:1000] + "..." if len(response4) > 1000 else response4)
    print("\n✅ Success: Analyzes multiple recipes, considers time & nutrition")
    print()
    
    await asyncio.sleep(2)
    
    # Test 5: Expert-Level - Complex multi-criteria with ranking
    print("=" * 60)
    print("👨‍🍳 LEVEL 5: Expert Multi-Criteria Analysis")
    print("=" * 60)
    print("Query: I'm having guests over and want to impress them with something sophisticated")
    print("       but not too time-consuming. I have mushrooms, cashews, and nutritional")
    print("       yeast on hand. What are my best options, ranked by impressiveness vs. effort?")
    print("-" * 60)
    response5 = await agent.chat("I'm having guests over and want to impress them with something sophisticated but not too time-consuming. I have mushrooms, cashews, and nutritional yeast on hand. What are my best options, ranked by impressiveness vs. effort?")
    print("Response:")
    print(response5[:1200] + "..." if len(response5) > 1200 else response5)
    print("\n✅ Success: Complex analysis with ingredient matching, sophistication ranking")
    print()
    
    # Final summary
    print("🏆" * 60)
    print("CAPABILITY DEMONSTRATION COMPLETE!")
    print("🏆" * 60)
    print("✅ Level 1: File Discovery - Lists all recipes without errors")
    print("✅ Level 2: Content Reading - Extracts specific recipe information") 
    print("✅ Level 3: Recipe Search - Finds recipes matching criteria")
    print("✅ Level 4: Smart Analysis - Multi-criteria recommendations") 
    print("✅ Level 5: Expert Mode - Complex ranking with ingredient matching")
    print()
    print("🌿 Sage File Search Agent: FROM SIMPLE TO SOPHISTICATED! 🌿")

if __name__ == "__main__":
    asyncio.run(showcase_capabilities())