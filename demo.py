#!/usr/bin/env python3
"""
Live Demo of Sage File Search Agent
"""
import asyncio
from sage_agent_tiny import SageAgent

async def demo_agent():
    """Demonstrate all 5 levels of file search capability"""
    print("🌿" * 30)
    print("   SAGE FILE SEARCH AGENT DEMO")
    print("🌿" * 30)
    print()
    
    agent = SageAgent()
    
    demos = [
        ("Test 1: Basic Discovery", "What recipe files do you have available?"),
        ("Test 2: Content Reading", "Show me the ingredients in the Cashew Alfredo recipe"),
        ("Test 3: Recipe Search", "Find me vegan pasta recipes"),
        ("Test 4: Analysis & Recommendation", "I want to make something quick for lunch that's high in protein. What do you recommend and why?"),
        ("Test 5: Multi-Criteria Ranking", "I'm having guests over and want to impress them with something sophisticated but not too time-consuming. I have mushrooms, cashews, and nutritional yeast on hand. What are my best options, ranked by impressiveness vs. effort?")
    ]
    
    for i, (title, query) in enumerate(demos, 1):
        print(f"{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
        print(f"Query: {query}")
        print(f"{'-'*60}")
        
        try:
            response = await agent.chat(query)
            # Truncate very long responses for demo
            if len(response) > 2000:
                response = response[:2000] + "\n\n... [response truncated for demo] ..."
            print(f"Sage: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        if i < len(demos):
            input("Press Enter to continue to next demo...")
        print()

if __name__ == "__main__":
    asyncio.run(demo_agent())