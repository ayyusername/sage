#!/usr/bin/env python3
"""
Test Version 1.1 prompt
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_v11_prompt():
    """Test the Version 1.1 prompt"""
    
    new_prompt = """You are Sage, a precise culinary AI assistant. You have access to recipe files through tools.

MANDATORY WORKFLOW FOR INGREDIENT SEARCHES:
1. ALWAYS call list_directory first to see available files
2. MUST call read_multiple_files or read_file to check actual contents
3. ONLY make ingredient claims based on what you read in file contents
4. NEVER assume ingredients from filenames alone

CRITICAL ACCURACY REQUIREMENTS:
- If user asks about ingredients: YOU MUST READ FILE CONTENTS FIRST
- NEVER claim "recipe contains X" without reading the actual recipe text
- When information is not found in file contents, say so clearly
- Be helpful by being truthful, not by making assumptions

TOOL CALL FORMAT:
TOOL_CALL: {"name": "tool_name", "parameters": {"param": "value"}}

Available tools:
- list_directory: {"path": "/Users/josh/Rose/sage/test-recipes/"} - Lists actual files
- read_file: {"path": "/Users/josh/Rose/sage/test-recipes/actual-filename.md"} - Use real filenames only
- read_multiple_files: {"paths": ["actual-file1.md", "actual-file2.md"]} - Use real filenames only

EXAMPLES:
User: "Find recipes with olive oil"
WRONG: List files and assume ingredients
RIGHT: List files, then read files, then check contents for "olive oil\""""
    
    print("🧪 TESTING PROMPT VERSION 1.1")
    print("=" * 50)
    print("Key change: Mandatory workflow for ingredient searches")
    print()
    
    # Test olive oil case
    agent = SageAgentDebug()
    
    # Override the chat method to use our new prompt
    original_chat = agent.chat
    async def chat_with_new_prompt(message, temperature=0.1):
        if not agent.client:
            await agent.initialize()
            
        agent.log_event("USER_MESSAGE", message, {"temperature": temperature})
        agent.log_event("SYSTEM_PROMPT", f"Using NEW prompt v1.1 ({len(new_prompt)} chars)")
        
        messages = [
            {"role": "system", "content": new_prompt},
            {"role": "user", "content": message}
        ]
        
        # Continue with normal flow
        response = await agent.call_llm(messages, temperature)
        
        # Check for tool calls and execute
        if "TOOL_CALL:" in response:
            try:
                # Extract tool call
                tool_start = response.find("TOOL_CALL:") + 10
                tool_json = response[tool_start:].strip()
                
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
                
                # Generate final response
                final_messages = [
                    {"role": "system", "content": "Provide a response based ONLY on the tool results below."},
                    {"role": "user", "content": f"User asked: {message}"},
                    {"role": "user", "content": f"Tool results: {tool_result}"},
                    {"role": "user", "content": "Based ONLY on these tool results, what is your response?"}
                ]
                
                agent.log_event("FINAL_LLM_CALL", "Generating final response based on tool results")
                final_response = await agent.call_llm(final_messages, temperature)
                
                return final_response
                
            except Exception as e:
                agent.log_event("TOOL_PARSE_ERROR", f"Error: {e}")
                return response
        
        return response
    
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
    asyncio.run(test_v11_prompt())