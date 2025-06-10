#!/usr/bin/env python3
"""
Test the agent on your actual Obsidian vault recipe files
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_obsidian_vault():
    """Test agent on real Obsidian vault recipes"""
    
    # Update prompt to use your Obsidian vault path
    obsidian_prompt = """You are Sage, a culinary AI assistant. You have access to recipe files through tools.

MANDATORY PROCESS for ingredient questions:

STEP 1: Get the list of files
TOOL_CALL: {"name": "list_directory", "parameters": {"path": "/Users/josh/ObsidianVault/recipetests/"}}

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
    
    print("🗂️  TESTING OBSIDIAN VAULT RECIPES")
    print("=" * 60)
    print("Path: /Users/josh/ObsidianVault/recipetests/")
    print()
    
    agent = SageAgentDebug()
    await agent.initialize()
    
    # Helper function to execute agent with Obsidian prompt
    async def obsidian_chat(message):
        agent.log_event("USER_MESSAGE", message)
        agent.log_event("SYSTEM_PROMPT", f"Using Obsidian prompt ({len(obsidian_prompt)} chars)")
        
        messages = [
            {"role": "system", "content": obsidian_prompt},
            {"role": "user", "content": message}
        ]
        
        response = await agent.call_llm(messages, 0.1)
        
        # Execute tool calls
        remaining_response = response
        tool_results = []
        
        while "TOOL_CALL:" in remaining_response:
            try:
                # Extract tool call
                tool_start = remaining_response.find("TOOL_CALL:") + 10
                tool_json = remaining_response[tool_start:].strip()
                
                json_start = tool_json.find("{")
                brace_count = 0
                json_end = json_start
                
                for i, char in enumerate(tool_json[json_start:], json_start):
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break
                
                tool_call_str = tool_json[json_start:json_end]
                agent.log_event("TOOL_CALL_PARSED", f"Parsed: {tool_call_str}")
                
                import json
                tool_call = json.loads(tool_call_str)
                tool_name = tool_call["name"]
                parameters = tool_call["parameters"]
                
                # Execute the tool
                tool_result = agent.execute_tool(tool_name, parameters)
                tool_results.append(tool_result)
                
                # Move past this tool call
                remaining_response = remaining_response[remaining_response.find("TOOL_CALL:") + len(tool_call_str) + 10:]
                
            except Exception as e:
                agent.log_event("TOOL_ERROR", f"Error executing tool: {e}")
                break
        
        # Generate final response based on tool results
        if tool_results:
            final_messages = [
                {"role": "system", "content": "Based on the tool results below, provide your final answer. Only mention ingredients you actually found in the file contents."},
                {"role": "user", "content": f"User asked: {message}"},
                {"role": "user", "content": f"Tool results: {' '.join(tool_results)}"},
                {"role": "user", "content": "What is your final answer?"}
            ]
            
            final_response = await agent.call_llm(final_messages, 0.1)
            return final_response
        
        return response
    
    agent.chat = obsidian_chat
    
    # Test 1: Discover what's in the Obsidian vault
    print("📁 TEST 1: Obsidian Vault Discovery")
    print("-" * 40)
    response1 = await agent.chat("What recipe files are in my Obsidian vault?")
    print(f"Response: {response1}")
    
    print(f"\n📊 VAULT CONTENTS ANALYSIS:")
    file_reads = [log for log in agent.conversation_log if log.get("type") == "FILE_READ_SUCCESS"]
    tool_calls = [log for log in agent.conversation_log if log.get("type") == "TOOL_CALL"]
    directory_results = [log for log in agent.conversation_log if log.get("type") == "TOOL_RESULT" and "Found" in log.get("content", "")]
    
    if directory_results:
        print(f"✅ Vault accessible: {directory_results[-1]['content']}")
    else:
        print(f"❌ Could not access vault")
        return False
    
    # Test 2: Try an ingredient search on real vault files
    print(f"\n🔍 TEST 2: Ingredient Search in Vault")
    print("-" * 40)
    response2 = await agent.chat("Find recipes that contain garlic")
    print(f"Response: {response2}")
    
    # Test 3: Try cumin search (should be honest if not found)
    print(f"\n🧪 TEST 3: Honesty Test (Cumin)")
    print("-" * 40)
    response3 = await agent.chat("Find recipes that contain cumin")
    print(f"Response: {response3}")
    
    # Final analysis
    file_reads_final = [log for log in agent.conversation_log if log.get("type") == "FILE_READ_SUCCESS"]
    
    print(f"\n📊 FINAL ANALYSIS")
    print("=" * 40)
    print(f"Total tool calls: {len(tool_calls)}")
    print(f"Successful file reads: {len(file_reads_final)}")
    
    if file_reads_final:
        print(f"✅ SUCCESS: Agent can read your Obsidian vault!")
        print(f"Files read from vault:")
        for read in file_reads_final:
            file_info = read.get("extra_data", {})
            print(f"  - {file_info.get('file', 'unknown')}: {file_info.get('size', 0)} chars")
    else:
        print(f"⚠️  Agent accessed vault but didn't read file contents yet")
    
    return len(file_reads_final) > 0

if __name__ == "__main__":
    asyncio.run(test_obsidian_vault())