#!/usr/bin/env python3
"""
Test if the agent can actually read real files on your computer
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_real_file_reading():
    """Test if agent can read actual files"""
    
    winning_prompt = """You are Sage, a culinary AI assistant. You have access to recipe files through tools.

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
    
    print("🔍 TESTING REAL FILE READING CAPABILITY")
    print("=" * 60)
    
    agent = SageAgentDebug()
    await agent.initialize()
    
    # Override system prompt for this test
    async def chat_with_winning_prompt(message):
        agent.log_event("USER_MESSAGE", message)
        agent.log_event("SYSTEM_PROMPT", f"Using winning prompt v1.3 ({len(winning_prompt)} chars)")
        
        messages = [
            {"role": "system", "content": winning_prompt},
            {"role": "user", "content": message}
        ]
        
        response = await agent.call_llm(messages, 0.1)
        
        # Execute any tool calls the agent makes
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
    
    agent.chat = chat_with_winning_prompt
    
    # Test 1: Check what files exist
    print("📁 TEST 1: File Discovery")
    print("-" * 30)
    response1 = await agent.chat("What recipe files do you have access to?")
    print(f"Response: {response1}")
    
    # Test 2: Try to read a specific file 
    print(f"\n📄 TEST 2: Specific File Reading")
    print("-" * 30)
    response2 = await agent.chat("Show me the contents of pasta-aglio-e-olio.md")
    print(f"Response: {response2[:200]}..." if len(response2) > 200 else response2)
    
    # Test 3: Ingredient search that should work
    print(f"\n🔍 TEST 3: Ingredient Search (Olive Oil)")
    print("-" * 30)
    response3 = await agent.chat("Find recipes that contain olive oil")
    print(f"Response: {response3}")
    
    # Analyze the results
    file_reads = [log for log in agent.conversation_log if log.get("type") == "FILE_READ_SUCCESS"]
    tool_calls = [log for log in agent.conversation_log if log.get("type") == "TOOL_CALL"]
    
    print(f"\n📊 ANALYSIS")
    print("=" * 30)
    print(f"Total tool calls: {len(tool_calls)}")
    print(f"Successful file reads: {len(file_reads)}")
    
    if file_reads:
        print(f"✅ SUCCESS: Agent can read real files!")
        for read in file_reads:
            file_info = read.get("extra_data", {})
            print(f"  - Read {file_info.get('file', 'unknown')}: {file_info.get('size', 0)} chars")
    else:
        print(f"❌ ISSUE: Agent is not reading actual file contents")
    
    return len(file_reads) > 0

if __name__ == "__main__":
    asyncio.run(test_real_file_reading())