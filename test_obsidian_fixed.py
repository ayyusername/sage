#!/usr/bin/env python3
"""
Fixed test for Obsidian vault - properly read the actual vault files
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_obsidian_fixed():
    """Test agent on Obsidian vault with proper file handling"""
    
    print("🗂️  FIXED OBSIDIAN VAULT TEST")
    print("=" * 60)
    
    agent = SageAgentDebug()
    await agent.initialize()
    
    # Test 1: See what's actually in the vault
    print("📁 STEP 1: Check what files exist in vault")
    print("-" * 40)
    
    vault_files = agent.execute_tool("list_directory", {"path": "/Users/josh/ObsidianVault/recipetests/"})
    print(f"Vault contents: {vault_files}")
    
    # Test 2: Read one specific file to verify access
    print(f"\n📄 STEP 2: Try to read a specific vault file")
    print("-" * 40)
    
    # Try to read the Chana Masala file
    chana_result = agent.execute_tool("read_file", {"path": "/Users/josh/ObsidianVault/recipetests/Chana Masala - YFL.md"})
    print(f"Chana Masala file: {chana_result[:200]}..." if len(chana_result) > 200 else chana_result)
    
    # Test 3: Read multiple vault files
    print(f"\n📚 STEP 3: Read multiple vault files")
    print("-" * 40)
    
    # Use actual vault filenames
    vault_filenames = ["Chana Masala - YFL.md", "Beef and Broccoli.md", "Ginger Syrup.md", "Vegan Beef Wellington.md"]
    
    multi_result = agent.execute_tool("read_multiple_files", {"paths": vault_filenames})
    
    # Check what we got
    if "File not found" in multi_result:
        print(f"❌ Issue reading vault files: {multi_result[:300]}...")
    else:
        print(f"✅ Successfully read vault files: {len(multi_result)} chars total")
        print(f"Sample: {multi_result[:200]}...")
    
    # Test 4: Manual ingredient search
    print(f"\n🔍 STEP 4: Manual ingredient search in vault content")
    print("-" * 40)
    
    if "File not found" not in multi_result:
        # Search for specific ingredients in the content
        content_lower = multi_result.lower()
        
        ingredients_to_check = ["garlic", "cumin", "ginger", "onion", "beef"]
        
        for ingredient in ingredients_to_check:
            found = ingredient in content_lower
            print(f"  {ingredient}: {'✅ Found' if found else '❌ Not found'}")
    
    # Test 5: Agent-driven search with corrected prompt
    print(f"\n🤖 STEP 5: Agent-driven search with vault-specific prompt")
    print("-" * 40)
    
    # Create a vault-specific prompt that forces the agent to use vault files
    vault_prompt = f"""You are Sage, a culinary AI assistant with access to Obsidian vault recipe files.

MANDATORY PROCESS for ingredient questions:

STEP 1: Get the list of files
TOOL_CALL: {{"name": "list_directory", "parameters": {{"path": "/Users/josh/ObsidianVault/recipetests/"}}}}

STEP 2: Read ONLY the actual files from the vault (use exact filenames from step 1)
Available files: Beef and Broccoli.md, Chana Masala - YFL.md, Ginger Syrup.md, Vegan Beef Wellington.md

CRITICAL RULES:
- ONLY use filenames that exist in the vault
- NEVER make up filenames 
- Read actual vault files at /Users/josh/ObsidianVault/recipetests/
- Only claim ingredients exist if found in actual file contents"""
    
    messages = [
        {"role": "system", "content": vault_prompt},
        {"role": "user", "content": "Find recipes that contain ginger"}
    ]
    
    response = await agent.call_llm(messages, 0.1)
    print(f"Agent response: {response}")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_obsidian_fixed())