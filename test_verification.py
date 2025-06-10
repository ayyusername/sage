#!/usr/bin/env python3
"""
Test to verify the agent actually reads files before making ingredient claims
"""
import asyncio
from sage_agent_production import SageAgentProduction

async def test_file_reading():
    """Test that agent reads files before claiming ingredients"""
    agent = SageAgentProduction()
    await agent.initialize()
    
    print("🔍 FILE READING VERIFICATION TEST")
    print("=" * 50)
    
    # Test 1: Ask for a specific ingredient and see if it reads files
    print("\n1️⃣ GARLIC SEARCH - Should read actual files")
    print("-" * 40)
    response = await agent.chat("Which recipes contain garlic? Please read the actual recipe files to check.")
    print(f"Response: {response}")
    
    # Check if response mentions specific files or just guesses
    mentions_reading = any(phrase in response.lower() for phrase in 
                          ["read", "checked", "searched through", "found in"])
    print(f"✅ Mentions reading files: {mentions_reading}")
    
    # Test 2: Ask for nutritional yeast (probably not in our simple recipes)
    print("\n2️⃣ NUTRITIONAL YEAST SEARCH")
    print("-" * 40)
    response = await agent.chat("Find recipes that use nutritional yeast")
    print(f"Response: {response}")
    
    honest_about_ny = any(phrase in response.lower() for phrase in 
                         ["not found", "could not find", "don't have"])
    print(f"✅ Honest about nutritional yeast: {honest_about_ny}")
    
    # Test 3: Direct file request to see if it uses actual filenames
    print("\n3️⃣ SPECIFIC FILE REQUEST")
    print("-" * 40)
    response = await agent.chat("Show me the vegan-kimchi.md recipe")
    print(f"Response: {response}")
    
    uses_real_file = "vegan-kimchi" in response.lower()
    print(f"✅ Uses actual filename: {uses_real_file}")

if __name__ == "__main__":
    asyncio.run(test_file_reading())