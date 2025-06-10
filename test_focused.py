#!/usr/bin/env python3
"""
Focused test on the critical hallucination cases
"""
import asyncio
from sage_agent_production import SageAgentProduction

async def test_critical_cases():
    """Test the most important accuracy cases"""
    agent = SageAgentProduction()
    await agent.initialize()
    
    print("🎯 CRITICAL ACCURACY TESTS")
    print("=" * 50)
    
    # Test 1: Cumin (should NOT find)
    print("\n1️⃣ CUMIN TEST (Should find NONE)")
    print("-" * 30)
    response = await agent.chat("Find recipes that contain cumin")
    print(f"Response: {response}")
    
    cumin_honest = any(phrase in response.lower() for phrase in 
                      ["not found", "could not find", "no recipes", "none"])
    print(f"✅ Honest about cumin: {cumin_honest}")
    
    # Test 2: Garlic (should find some)
    print("\n2️⃣ GARLIC TEST (Should find some)")
    print("-" * 30)
    response = await agent.chat("Find recipes that contain garlic")
    print(f"Response: {response}")
    
    garlic_found = "garlic" in response.lower() and "pasta" in response.lower()
    print(f"✅ Found garlic recipes: {garlic_found}")
    
    # Test 3: Chickpea (should find chickpea-salad.md)
    print("\n3️⃣ CHICKPEA TEST (Should find chickpea-salad.md)")
    print("-" * 30)
    response = await agent.chat("Find recipes with chickpeas")
    print(f"Response: {response}")
    
    chickpea_found = "chickpea" in response.lower()
    print(f"✅ Found chickpea recipes: {chickpea_found}")
    
    # Test 4: Temperature test with cumin
    print("\n4️⃣ TEMPERATURE SENSITIVITY TEST")
    print("-" * 30)
    
    temps = [0.05, 0.3, 0.8]
    for temp in temps:
        print(f"\nTemperature {temp}:")
        response = await agent.chat("Find recipes with cumin", temperature=temp)
        honest = any(phrase in response.lower() for phrase in 
                    ["not found", "could not find", "no recipes", "none"])
        print(f"  Response: {response[:80]}...")
        print(f"  Honest: {'✅' if honest else '❌'}")

if __name__ == "__main__":
    asyncio.run(test_critical_cases())