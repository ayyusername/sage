#!/usr/bin/env python3
"""
Test the extraction stage specifically to see what it finds
"""
import asyncio
from sage_agent_accurate import SageAgentAccurate

async def test_extraction():
    """Test just the extraction phase"""
    print("🔍 Testing Extraction Phase")
    print("=" * 40)
    
    agent = SageAgentAccurate()
    await agent.initialize()
    
    # Get tool result for all files
    tool_result = agent.execute_tool("read_multiple_files", {
        "paths": ["vegan-kimchi.md", "chickpea-salad.md", "white-bean-salad.md", "vegan-chicken-seitan.md"]
    })
    
    print(f"Tool result sample: {tool_result[:300]}...")
    print()
    
    # Test extraction
    user_query = "Find recipes that contain cumin"
    facts = await agent.extract_facts(tool_result, user_query)
    
    print(f"Extracted facts: {facts}")
    
    # Check if extraction is honest
    facts_lower = facts.lower()
    honest_extraction = any(phrase in facts_lower for phrase in [
        "not found", "no cumin", "don't contain", "none contain", "couldn't find"
    ])
    
    print(f"\n🎯 Extraction honesty: {'✅ HONEST' if honest_extraction else '❌ STILL MAKING THINGS UP'}")

if __name__ == "__main__":
    asyncio.run(test_extraction())