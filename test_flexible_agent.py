#!/usr/bin/env python3
"""
Test the truly flexible agent that works with any directory
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_flexible_agent():
    """Test agent that works with any directory without hardcoding"""
    
    # Create a flexible prompt that can work with any directory
    def create_flexible_prompt(recipe_directory):
        return f"""You are Sage, a culinary AI assistant. You have access to recipe files through tools.

MANDATORY PROCESS for ingredient questions:

STEP 1: Get the list of files
TOOL_CALL: {{"name": "list_directory", "parameters": {{"path": "{recipe_directory}"}}}}

STEP 2: Read the ACTUAL files from step 1 (use the exact filenames shown)
TOOL_CALL: {{"name": "read_multiple_files", "parameters": {{"paths": ["exact-filename1.md", "exact-filename2.md"], "base_path": "{recipe_directory}"}}}}

STEP 3: Search the file contents for the ingredient
STEP 4: Report only what you found

CRITICAL RULES:
- MUST use exact filenames from list_directory result
- NEVER make up filenames like "recipe1.md" or "recipe2.md"  
- ONLY claim ingredients exist if you see them in actual file contents
- If files don't contain the ingredient, say so honestly

Example:
If list_directory shows: ["pasta-aglio-e-olio.md", "chickpea-salad.md"]
Then use: {{"paths": ["pasta-aglio-e-olio.md", "chickpea-salad.md"], "base_path": "{recipe_directory}"}}
NOT: {{"paths": ["recipe1.md", "recipe2.md"]}}"""

    print("🔧 TESTING TRULY FLEXIBLE AGENT")
    print("=" * 60)
    
    agent = SageAgentDebug()
    await agent.initialize()
    
    # Test 1: Original test recipes
    print("📁 TEST 1: Original test recipes")
    print("-" * 40)
    
    test_prompt = create_flexible_prompt("/Users/josh/Rose/sage/test-recipes/")
    messages1 = [
        {"role": "system", "content": test_prompt},
        {"role": "user", "content": "Find recipes that contain olive oil"}
    ]
    
    response1 = await agent.call_llm(messages1, 0.1)
    print(f"Test recipes response: {response1[:200]}...")
    
    # Test 2: Obsidian vault
    print(f"\n🗂️ TEST 2: Obsidian vault")
    print("-" * 40)
    
    vault_prompt = create_flexible_prompt("/Users/josh/ObsidianVault/recipetests/")
    messages2 = [
        {"role": "system", "content": vault_prompt},
        {"role": "user", "content": "Find recipes that contain ginger"}
    ]
    
    response2 = await agent.call_llm(messages2, 0.1)
    print(f"Vault response: {response2[:200]}...")
    
    # Test 3: Check what tool calls the agent makes
    print(f"\n🔍 ANALYSIS: Tool calls made")
    print("-" * 40)
    
    tool_calls = [log for log in agent.conversation_log if log.get("type") == "TOOL_CALL"]
    file_reads = [log for log in agent.conversation_log if log.get("type") == "FILE_READ_SUCCESS"]
    
    print(f"Total tool calls: {len(tool_calls)}")
    for i, call in enumerate(tool_calls[-6:], 1):  # Show last 6 calls
        print(f"  {i}. {call['content']}")
    
    print(f"\nFile reads: {len(file_reads)}")
    for read in file_reads[-4:]:  # Show last 4 reads
        extra = read.get("extra_data", {})
        print(f"  - {extra.get('file', 'unknown')}: {extra.get('size', 0)} chars")
    
    # Test 4: Interactive mode
    print(f"\n💬 INTERACTIVE TEST")
    print("-" * 40)
    print("This agent can now work with ANY directory you specify!")
    print("Just change the path in create_flexible_prompt() function")
    
    return len(file_reads) > 0

if __name__ == "__main__":
    asyncio.run(test_flexible_agent())