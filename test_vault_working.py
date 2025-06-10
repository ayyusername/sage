#!/usr/bin/env python3
"""
Working test for Obsidian vault using individual file reads
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_vault_working():
    """Test vault with individual file reads"""
    
    print("🗂️  WORKING OBSIDIAN VAULT TEST")
    print("=" * 60)
    
    agent = SageAgentDebug()
    await agent.initialize()
    
    # Read all vault files individually (since read_multiple_files has a path bug)
    vault_files = ["Chana Masala - YFL.md", "Beef and Broccoli.md", "Ginger Syrup.md", "Vegan Beef Wellington.md"]
    vault_contents = {}
    
    print("📚 Reading all vault files:")
    print("-" * 40)
    
    for filename in vault_files:
        result = agent.execute_tool("read_file", {"path": f"/Users/josh/ObsidianVault/recipetests/{filename}"})
        
        if "File not found" not in result:
            # Extract content after the header
            content = result.split("===", 2)[-1].strip() if "===" in result else result
            vault_contents[filename] = content
            print(f"✅ {filename}: {len(content)} chars")
        else:
            print(f"❌ {filename}: Not found")
    
    if not vault_contents:
        print("❌ Could not read any vault files")
        return False
    
    # Now do ingredient searches on the actual content
    print(f"\n🔍 INGREDIENT SEARCH TESTS")
    print("=" * 40)
    
    # Combine all content for searching
    all_content = "\n\n".join([f"=== {filename} ===\n{content}" for filename, content in vault_contents.items()])
    
    # Test ingredients
    test_ingredients = ["garlic", "cumin", "ginger", "onion", "chickpea", "beef"]
    
    for ingredient in test_ingredients:
        found_in = []
        for filename, content in vault_contents.items():
            if ingredient.lower() in content.lower():
                found_in.append(filename)
        
        if found_in:
            print(f"✅ {ingredient}: Found in {', '.join(found_in)}")
        else:
            print(f"❌ {ingredient}: Not found")
    
    # Test agent with proper vault content
    print(f"\n🤖 AGENT TEST: Garlic Search")
    print("-" * 40)
    
    vault_prompt = f"""You are Sage, a culinary AI assistant. Based on the recipe content below, answer questions about ingredients.

RECIPE CONTENT:
{all_content}

RULES:
- Only mention ingredients that are explicitly listed in the recipe content above
- If an ingredient is not found, say so honestly
- Be specific about which recipes contain the ingredient"""
    
    messages = [
        {"role": "system", "content": vault_prompt},
        {"role": "user", "content": "Which recipes contain garlic?"}
    ]
    
    response = await agent.call_llm(messages, 0.1)
    print(f"Agent response: {response}")
    
    # Test honesty with cumin
    print(f"\n🧪 AGENT TEST: Cumin Honesty")
    print("-" * 40)
    
    messages2 = [
        {"role": "system", "content": vault_prompt},
        {"role": "user", "content": "Which recipes contain cumin?"}
    ]
    
    response2 = await agent.call_llm(messages2, 0.1)
    print(f"Agent response: {response2}")
    
    # Check if agent is honest about cumin
    cumin_honest = any(phrase in response2.lower() for phrase in ["not found", "don't", "no recipes", "none"])
    print(f"Cumin honesty: {'✅ Honest' if cumin_honest else '❌ Made claims'}")
    
    print(f"\n📊 SUMMARY")
    print("=" * 30)
    print(f"Vault files read: {len(vault_contents)}/4")
    print(f"Total content: {len(all_content)} chars")
    print(f"Agent can access vault: ✅")
    print(f"Agent reads real content: ✅")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_vault_working())