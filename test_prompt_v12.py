#!/usr/bin/env python3
"""
Test Version 1.2 prompt - Force two-step process
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_v12_prompt():
    """Test the Version 1.2 prompt with forced two-step process"""
    
    new_prompt = """You are Sage, a culinary AI assistant. You have access to recipe files through tools.

CRITICAL: For ANY ingredient question, you MUST follow this EXACT sequence:

STEP 1: Call list_directory to see available files
STEP 2: Call read_multiple_files with the actual filenames to read their contents  
STEP 3: Search the file contents for the ingredient
STEP 4: Only then provide your answer

YOU ARE FORBIDDEN from making ingredient claims after only calling list_directory.

If user asks about ingredients in recipes:
1. TOOL_CALL: {"name": "list_directory", "parameters": {"path": "/Users/josh/Rose/sage/test-recipes/"}}
2. TOOL_CALL: {"name": "read_multiple_files", "parameters": {"paths": ["actual-file1.md", "actual-file2.md"]}}
3. Check the actual file contents for the ingredient
4. Report only what you found in the file contents

NEVER guess ingredients from filenames. ALWAYS read file contents first."""
    
    print("🧪 TESTING PROMPT VERSION 1.2")
    print("=" * 50)
    print("Key change: FORBIDDEN from making claims after only list_directory")
    print()
    
    agent = SageAgentDebug()
    
    # Override system prompt
    async def chat_with_new_prompt(message, temperature=0.1):
        if not agent.client:
            await agent.initialize()
            
        agent.log_event("USER_MESSAGE", message, {"temperature": temperature})
        agent.log_event("SYSTEM_PROMPT", f"Using FORCED prompt v1.2 ({len(new_prompt)} chars)")
        
        messages = [
            {"role": "system", "content": new_prompt},
            {"role": "user", "content": message}
        ]
        
        response = await agent.call_llm(messages, temperature)
        
        # Check for tool calls - NOTE: Agent might make multiple tool calls
        remaining_response = response
        
        while "TOOL_CALL:" in remaining_response:
            try:
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
                agent.log_event("TOOL_CALL_PARSED", f"Parsed tool call: {tool_call_str}")
                
                import json
                tool_call = json.loads(tool_call_str)
                tool_name = tool_call["name"]
                parameters = tool_call["parameters"]
                
                # Execute tool
                tool_result = agent.execute_tool(tool_name, parameters)
                
                # Remove this tool call and continue looking for more
                remaining_response = remaining_response[remaining_response.find("TOOL_CALL:") + len(tool_call_str) + 10:]
                
            except Exception as e:
                agent.log_event("TOOL_PARSE_ERROR", f"Error: {e}")
                break
        
        # Generate final response
        final_messages = [
            {"role": "system", "content": "Provide a final response based on the tool results. Only mention ingredients you found in the actual file contents."},
            {"role": "user", "content": f"User asked: {message}"},
            {"role": "user", "content": "Provide your final answer based on what you found:"}
        ]
        
        agent.log_event("FINAL_LLM_CALL", "Generating final response")
        final_response = await agent.call_llm(final_messages, temperature)
        
        return final_response
    
    agent.chat = chat_with_new_prompt
    
    response = await agent.chat("Find recipes that contain olive oil")
    
    # Analyze results
    file_reads = [log for log in agent.conversation_log if log.get("type") == "FILE_READ_SUCCESS"]
    tool_calls = [log for log in agent.conversation_log if log.get("type") == "TOOL_CALL"]
    
    print(f"Response: {response}")
    print(f"\n📊 Analysis:")
    print(f"Tool calls: {len(tool_calls)}")
    for tool in tool_calls:
        print(f"  - {tool['content']}")
    print(f"File reads: {len(file_reads)}")
    for read in file_reads:
        print(f"  - {read['content']}")
    
    success = len(file_reads) > 0
    print(f"\n🎯 SUCCESS: {'✅' if success else '❌'} - {'Files read' if success else 'No file reads'}")
    
    return success

if __name__ == "__main__":
    asyncio.run(test_v12_prompt())