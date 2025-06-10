#!/usr/bin/env python3
"""
Test Version 1.3 prompt - Force real filenames
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_v13_prompt():
    """Test the Version 1.3 prompt with real filenames"""
    
    new_prompt = """You are Sage, a culinary AI assistant. You have access to recipe files through tools.

MANDATORY PROCESS for ingredient questions:

STEP 1: Get the list of files
TOOL_CALL: {"name": "list_directory", "parameters": {"path": "/Users/josh/Rose/sage/test-recipes/"}}

STEP 2: Read the ACTUAL files from step 1 (use the exact filenames shown)
TOOL_CALL: {"name": "read_multiple_files", "parameters": {"paths": ["exact-filename1.md", "exact-filename2.md"]}}

STEP 3: Search the file contents for the ingredient
STEP 4: Report only what you found

CRITICAL RULES:
- MUST use exact filenames from list_directory result
- NEVER make up filenames like "recipe1.md" or "recipe2.md"  
- ONLY claim ingredients exist if you see them in actual file contents
- If files don't contain the ingredient, say so honestly

Example:
If list_directory shows: ["pasta-aglio-e-olio.md", "chickpea-salad.md"]
Then use: {"paths": ["pasta-aglio-e-olio.md", "chickpea-salad.md"]}
NOT: {"paths": ["recipe1.md", "recipe2.md"]}"""
    
    print("🧪 TESTING PROMPT VERSION 1.3")
    print("=" * 50)
    print("Key change: Force exact filenames from directory listing")
    print()
    
    agent = SageAgentDebug()
    await agent.initialize()
    
    # Use the new prompt directly
    messages = [
        {"role": "system", "content": new_prompt},
        {"role": "user", "content": "Find recipes that contain olive oil"}
    ]
    
    agent.log_event("USER_MESSAGE", "Find recipes that contain olive oil")
    agent.log_event("SYSTEM_PROMPT", f"Using v1.3 prompt ({len(new_prompt)} chars)")
    
    response = await agent.call_llm(messages, 0.1)
    
    print(f"Initial response: {response}")
    print("\n" + "="*50)
    
    # Let's manually check what tool calls the agent wants to make
    if "TOOL_CALL:" in response:
        import re
        tool_calls = re.findall(r'TOOL_CALL:\s*({[^}]+})', response)
        print(f"Found {len(tool_calls)} tool calls:")
        for i, call in enumerate(tool_calls, 1):
            print(f"  {i}. {call}")
    
    # Analyze what we got
    file_reads = [log for log in agent.conversation_log if log.get("type") == "FILE_READ_SUCCESS"]
    tool_calls_made = [log for log in agent.conversation_log if log.get("type") == "TOOL_CALL"]
    
    print(f"\n📊 Analysis:")
    print(f"Tool calls made: {len(tool_calls_made)}")
    print(f"File reads: {len(file_reads)}")
    
    # Check if response shows the right intent
    wants_real_files = any(name in response for name in ["pasta-aglio-e-olio", "chickpea-salad", "vegan-kimchi"])
    avoids_fake_names = not any(fake in response for fake in ["recipe1.md", "recipe2.md", "filename1.md"])
    
    print(f"Uses real filenames: {'✅' if wants_real_files else '❌'}")
    print(f"Avoids fake names: {'✅' if avoids_fake_names else '❌'}")
    
    return wants_real_files and avoids_fake_names

if __name__ == "__main__":
    asyncio.run(test_v13_prompt())