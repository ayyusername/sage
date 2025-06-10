#!/usr/bin/env python3
"""
Sage Agent Debug - Enhanced version with full conversation logging
"""
import json
import asyncio
import os
from datetime import datetime
from openai import OpenAI

class SageAgentDebug:
    """Debug version with comprehensive logging"""
    
    def __init__(self, config_path: str = "sage_agent_config.json"):
        self.config_path = config_path
        self.client = None
        self.config = None
        self.conversation_log = []
        self.tool_calls_log = []
        
    async def load_config(self):
        """Load configuration"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        return self.config
        
    async def initialize(self):
        """Initialize OpenAI client"""
        config = await self.load_config()
        
        self.client = OpenAI(
            base_url=config["base_url"],
            api_key=config["api_key"]
        )
        
        self.log_event("SYSTEM", "🌿 Sage Agent Debug initialized")
        self.log_event("SYSTEM", f"✅ LM Studio: {config['base_url']}")
        
    def log_event(self, event_type: str, content: str, extra_data: dict = None):
        """Log all events with timestamps"""
        timestamp = datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "type": event_type,
            "content": content,
            "extra_data": extra_data or {}
        }
        self.conversation_log.append(event)
        print(f"[{timestamp}] {event_type}: {content}")
        
    def execute_tool(self, tool_name: str, parameters: dict) -> str:
        """Execute file operations with detailed logging"""
        
        self.log_event("TOOL_CALL", f"Executing {tool_name}", {"parameters": parameters})
        
        if tool_name == "list_directory":
            path = parameters.get("path", "/Users/josh/Rose/sage/test-recipes/")
            if os.path.exists(path):
                files = os.listdir(path)
                recipe_files = [f for f in files if f.endswith('.md')]
                result = f"Recipe files found ({len(recipe_files)}): {', '.join(recipe_files)}"
                self.log_event("TOOL_RESULT", f"Found {len(recipe_files)} files", {"files": recipe_files})
                return result
            else:
                result = f"Directory not found: {path}"
                self.log_event("TOOL_ERROR", result)
                return result
                
        elif tool_name == "read_file":
            path = parameters.get("path", "")
            self.log_event("FILE_READ_ATTEMPT", f"Trying to read: {path}")
            
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.read()
                result = f"=== File: {os.path.basename(path)} ===\n{content}"
                
                self.log_event("FILE_READ_SUCCESS", f"Read {len(content)} chars from {os.path.basename(path)}", {
                    "file_size": len(content),
                    "first_100_chars": content[:100],
                    "line_count": len(content.split('\n'))
                })
                return result
            else:
                result = f"File not found: {path}"
                self.log_event("FILE_READ_ERROR", result)
                return result
                
        elif tool_name == "read_multiple_files":
            paths = parameters.get("paths", [])
            base_path = parameters.get("base_path", "/Users/josh/Rose/sage/test-recipes/")
            self.log_event("MULTI_FILE_READ", f"Reading {len(paths)} files from {base_path}", {"paths": paths, "base_path": base_path})
            
            results = []
            for path in paths:
                # Use the base_path from parameters, or try to detect it from the path
                if path.startswith("/"):
                    # Absolute path provided
                    full_path = path
                else:
                    # Relative path - use base_path
                    full_path = os.path.join(base_path, path)
                
                self.log_event("FILE_READ_ATTEMPT", f"Reading: {full_path}")
                
                if os.path.exists(full_path):
                    with open(full_path, 'r') as f:
                        content = f.read()
                    results.append(f"\n=== {path} ===\n{content}")
                    
                    self.log_event("FILE_READ_SUCCESS", f"Read {path} ({len(content)} chars)", {
                        "file": path,
                        "size": len(content),
                        "preview": content[:100]
                    })
                else:
                    results.append(f"\n=== {path} ===\nFile not found")
                    self.log_event("FILE_READ_ERROR", f"File not found: {path}")
                    
            full_result = "".join(results)
            self.log_event("MULTI_FILE_RESULT", f"Combined result: {len(full_result)} chars total")
            return full_result
        else:
            result = f"Unknown tool: {tool_name}"
            self.log_event("TOOL_ERROR", result)
            return result
    
    async def call_llm(self, messages: list, temperature: float = 0.1) -> str:
        """Call LM Studio with detailed logging"""
        self.log_event("LLM_CALL", f"Calling LM Studio (temp: {temperature})", {
            "message_count": len(messages),
            "total_chars": sum(len(str(msg)) for msg in messages),
            "system_prompt_length": len(messages[0]["content"]) if messages else 0
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=messages,
                max_tokens=1000,
                temperature=temperature
            )
            result = response.choices[0].message.content
            
            self.log_event("LLM_RESPONSE", f"Received response ({len(result)} chars)", {
                "response_length": len(result),
                "first_100_chars": result[:100]
            })
            
            return result
        except Exception as e:
            error_msg = f"LLM Error: {e}"
            self.log_event("LLM_ERROR", error_msg)
            return error_msg
    
    def validate_response(self, response: str, tool_result: str, user_query: str) -> dict:
        """Validate response with detailed logging"""
        validation = {
            "hallucination_risk": "low",
            "warnings": [],
            "suggestions": []
        }
        
        response_lower = response.lower()
        query_lower = user_query.lower()
        
        self.log_event("VALIDATION_START", f"Validating response for hallucinations", {
            "response_length": len(response),
            "tool_result_length": len(tool_result)
        })
        
        # Check for ingredient claims when searching
        if any(keyword in query_lower for keyword in ["contain", "with", "has", "ingredient"]):
            # Extract potential ingredient mentions
            import re
            ingredient_pattern = r'\b(cumin|garlic|onion|tomato|pepper|salt|oil|lemon|cashew|nutritional yeast|ginger|turmeric)\b'
            claimed_ingredients = re.findall(ingredient_pattern, response_lower)
            
            for ingredient in claimed_ingredients:
                if ingredient not in tool_result.lower():
                    validation["hallucination_risk"] = "high"
                    validation["warnings"].append(f"Claims '{ingredient}' but not found in tool results")
                    validation["suggestions"].append(f"Remove mention of '{ingredient}' or state it was not found")
                    
                    self.log_event("HALLUCINATION_DETECTED", f"Ingredient '{ingredient}' claimed but not in tool results", {
                        "ingredient": ingredient,
                        "in_response": True,
                        "in_tool_result": False
                    })
        
        # Check for specific recipe claims
        if "recipe" in response_lower and ("contains" in response_lower or "has" in response_lower):
            validation["hallucination_risk"] = "medium"
            validation["warnings"].append("Making specific claims about recipe contents")
            self.log_event("VALIDATION_WARNING", "Agent making specific recipe content claims")
        
        self.log_event("VALIDATION_COMPLETE", f"Risk level: {validation['hallucination_risk']}", validation)
        return validation
    
    async def chat(self, message: str, temperature: float = 0.1) -> str:
        """Main chat with comprehensive logging"""
        if not self.client:
            await self.initialize()
            
        self.log_event("USER_MESSAGE", message, {"temperature": temperature})
            
        # Ultra-strict system prompt
        system_prompt = """You are Sage, a precise culinary AI assistant. You have access to recipe files through tools.

CRITICAL ACCURACY REQUIREMENTS:
1. ONLY state information that is EXPLICITLY present in tool results
2. NEVER add ingredients, cooking methods, or details not found in the actual file contents
3. When information is not found, say so clearly: "I could not find [X] in any of the recipe files"
4. Be helpful by being truthful, not by making assumptions
5. ALWAYS use list_directory first to see what files actually exist before trying to read them

TOOL USAGE WORKFLOW:
1. First, use list_directory to see what recipe files are actually available
2. Then, use the actual filenames shown in the directory listing
3. Base ALL responses on tool results, not on general culinary knowledge
4. If tool results are empty or don't contain requested information, state this honestly

EXAMPLES OF CORRECT RESPONSES:
- "I searched through all recipe files but none contain cumin"
- "Based on the recipe files I can access, here are the ones that actually mention garlic: [list from tool results]"
- "I don't see any recipes matching that criteria in the available files"

TOOL CALL FORMAT:
TOOL_CALL: {"name": "tool_name", "parameters": {"param": "value"}}

Available tools:
- list_directory: {"path": "/Users/josh/Rose/sage/test-recipes/"} - Lists actual files
- read_file: {"path": "/Users/josh/Rose/sage/test-recipes/actual-filename.md"} - Use real filenames only
- read_multiple_files: {"paths": ["actual-file1.md", "actual-file2.md"]} - Use real filenames only

CRITICAL: Never make up filenames! Always use list_directory first to see what files actually exist."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        self.log_event("SYSTEM_PROMPT", f"Using system prompt ({len(system_prompt)} chars)")
        
        # Get LLM response with low temperature for accuracy
        response = await self.call_llm(messages, temperature)
        
        # Check for tool calls
        if "TOOL_CALL:" in response:
            try:
                # Extract and execute tool call
                tool_start = response.find("TOOL_CALL:") + 10
                tool_json = response[tool_start:].strip()
                
                # Find complete JSON
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
                self.log_event("TOOL_CALL_PARSED", f"Parsed tool call: {tool_call_str}")
                
                tool_call = json.loads(tool_call_str)
                tool_name = tool_call["name"]
                parameters = tool_call["parameters"]
                
                # Execute tool
                tool_result = self.execute_tool(tool_name, parameters)
                
                # Generate response based on tool results with strict prompt
                final_messages = [
                    {"role": "system", "content": "You are Sage. Provide a response based ONLY on the tool results below. Do not add any information not explicitly stated in the tool results. If the requested information is not found in the tool results, state this clearly."},
                    {"role": "user", "content": f"User asked: {message}"},
                    {"role": "user", "content": f"Tool results: {tool_result}"},
                    {"role": "user", "content": "Based ONLY on these tool results, what is your response to the user?"}
                ]
                
                self.log_event("FINAL_LLM_CALL", "Generating final response based on tool results")
                final_response = await self.call_llm(final_messages, temperature)
                
                # Validate response for hallucinations
                validation = self.validate_response(final_response, tool_result, message)
                
                if validation["hallucination_risk"] == "high":
                    self.log_event("HALLUCINATION_PREVENTION", f"High risk detected, regenerating", validation)
                    
                    # Regenerate with even stricter prompt
                    strict_messages = [
                        {"role": "system", "content": "EMERGENCY ACCURACY MODE: Only state facts explicitly present in the tool results. If information is not found, say 'I could not find [X] in the recipe files.' Never make assumptions."},
                        {"role": "user", "content": f"User asked: {message}"},
                        {"role": "user", "content": f"Tool results: {tool_result}"},
                        {"role": "user", "content": "Provide an honest response about what you found (or didn't find):"}
                    ]
                    
                    corrected_response = await self.call_llm(strict_messages, 0.05)  # Ultra-low temperature
                    self.log_event("RESPONSE_REGENERATED", "Response regenerated with stricter accuracy")
                    return corrected_response
                
                return final_response
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                error_msg = f"Tool parsing error: {e}"
                self.log_event("TOOL_PARSE_ERROR", error_msg)
                return response
        
        return response
    
    def save_debug_log(self, filename: str = None):
        """Save complete debug log to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"debug_log_{timestamp}.json"
            
        debug_data = {
            "conversation_log": self.conversation_log,
            "total_events": len(self.conversation_log),
            "session_summary": {
                "llm_calls": len([e for e in self.conversation_log if e["type"] == "LLM_CALL"]),
                "tool_calls": len([e for e in self.conversation_log if e["type"] == "TOOL_CALL"]),
                "files_read": len([e for e in self.conversation_log if e["type"] == "FILE_READ_SUCCESS"]),
                "hallucinations_caught": len([e for e in self.conversation_log if e["type"] == "HALLUCINATION_DETECTED"])
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(debug_data, f, indent=2)
            
        self.log_event("DEBUG_SAVED", f"Debug log saved to {filename}")
        return filename

async def main():
    """Test the debug agent"""
    agent = SageAgentDebug()
    
    print("🔍 SAGE AGENT DEBUG SESSION")
    print("=" * 50)
    
    # Test queries that previously had issues
    test_queries = [
        "Find recipes that contain cumin",
        "Find recipes with olive oil",
        "What's in the chickpea-salad.md file?"
    ]
    
    for query in test_queries:
        print(f"\n🧪 Testing: {query}")
        print("-" * 30)
        
        response = await agent.chat(query)
        print(f"Final response: {response}")
        print()
    
    # Save debug log
    log_file = agent.save_debug_log()
    print(f"\n💾 Complete debug log saved to: {log_file}")

if __name__ == "__main__":
    asyncio.run(main())