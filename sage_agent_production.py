#!/usr/bin/env python3
"""
Sage Agent Production - Enhanced prompting with hallucination prevention
"""
import json
import asyncio
import os
import re
from openai import OpenAI

class SageAgentProduction:
    """Production-ready Sage agent with enhanced accuracy"""
    
    def __init__(self, config_path: str = "sage_agent_config.json"):
        self.config_path = config_path
        self.client = None
        self.config = None
        
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
        
        print("🌿 Sage Agent Production initialized")
        print(f"✅ LM Studio: {config['base_url']}")
        
    def execute_tool(self, tool_name: str, parameters: dict) -> str:
        """Execute file operations directly"""
        
        if tool_name == "list_directory":
            path = parameters.get("path", "/Users/josh/Rose/sage/test-recipes/")
            if os.path.exists(path):
                files = os.listdir(path)
                recipe_files = [f for f in files if f.endswith('.md')]
                return f"Recipe files found ({len(recipe_files)}): {', '.join(recipe_files)}"
            else:
                return f"Directory not found: {path}"
                
        elif tool_name == "read_file":
            path = parameters.get("path", "")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.read()
                return f"=== File: {os.path.basename(path)} ===\n{content}"
            else:
                return f"File not found: {path}"
                
        elif tool_name == "read_multiple_files":
            paths = parameters.get("paths", [])
            results = []
            
            for path in paths:
                full_path = f"/Users/josh/Rose/sage/test-recipes/{path}"
                if os.path.exists(full_path):
                    with open(full_path, 'r') as f:
                        content = f.read()
                    results.append(f"\n=== {path} ===\n{content}")
                else:
                    results.append(f"\n=== {path} ===\nFile not found")
                    
            return "".join(results)
        else:
            return f"Unknown tool: {tool_name}"
    
    async def call_llm(self, messages: list, temperature: float = 0.1) -> str:
        """Call LM Studio with specified temperature"""
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=messages,
                max_tokens=1000,
                temperature=temperature  # Override LM Studio setting
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Error: {e}"
    
    def validate_response(self, response: str, tool_result: str, user_query: str) -> dict:
        """Validate response for potential hallucinations"""
        validation = {
            "hallucination_risk": "low",
            "warnings": [],
            "suggestions": []
        }
        
        response_lower = response.lower()
        query_lower = user_query.lower()
        
        # Check for ingredient claims when searching
        if any(keyword in query_lower for keyword in ["contain", "with", "has", "ingredient"]):
            # Extract potential ingredient mentions
            ingredient_pattern = r'\b(cumin|garlic|onion|tomato|pepper|salt|oil|lemon|cashew|nutritional yeast|ginger|turmeric)\b'
            claimed_ingredients = re.findall(ingredient_pattern, response_lower)
            
            for ingredient in claimed_ingredients:
                if ingredient not in tool_result.lower():
                    validation["hallucination_risk"] = "high"
                    validation["warnings"].append(f"Claims '{ingredient}' but not found in tool results")
                    validation["suggestions"].append(f"Remove mention of '{ingredient}' or state it was not found")
        
        # Check for specific recipe claims
        if "recipe" in response_lower and ("contains" in response_lower or "has" in response_lower):
            validation["hallucination_risk"] = "medium"
            validation["warnings"].append("Making specific claims about recipe contents")
        
        return validation
    
    async def chat(self, message: str, temperature: float = 0.1) -> str:
        """Main chat with enhanced accuracy and validation"""
        if not self.client:
            await self.initialize()
            
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
                print(f"🔧 Executing: {tool_call_str}")
                
                tool_call = json.loads(tool_call_str)
                tool_name = tool_call["name"]
                parameters = tool_call["parameters"]
                
                # Execute tool
                tool_result = self.execute_tool(tool_name, parameters)
                print(f"📄 Tool result: {len(tool_result)} chars")
                
                # Generate response based on tool results with strict prompt
                final_messages = [
                    {"role": "system", "content": "You are Sage. Provide a response based ONLY on the tool results below. Do not add any information not explicitly stated in the tool results. If the requested information is not found in the tool results, state this clearly."},
                    {"role": "user", "content": f"User asked: {message}"},
                    {"role": "user", "content": f"Tool results: {tool_result}"},
                    {"role": "user", "content": "Based ONLY on these tool results, what is your response to the user?"}
                ]
                
                final_response = await self.call_llm(final_messages, temperature)
                
                # Validate response for hallucinations
                validation = self.validate_response(final_response, tool_result, message)
                
                if validation["hallucination_risk"] == "high":
                    print(f"⚠️  HIGH HALLUCINATION RISK: {validation['warnings']}")
                    
                    # Regenerate with even stricter prompt
                    strict_messages = [
                        {"role": "system", "content": "EMERGENCY ACCURACY MODE: Only state facts explicitly present in the tool results. If information is not found, say 'I could not find [X] in the recipe files.' Never make assumptions."},
                        {"role": "user", "content": f"User asked: {message}"},
                        {"role": "user", "content": f"Tool results: {tool_result}"},
                        {"role": "user", "content": "Provide an honest response about what you found (or didn't find):"}
                    ]
                    
                    corrected_response = await self.call_llm(strict_messages, 0.05)  # Ultra-low temperature
                    print("🔄 Regenerated response with stricter accuracy")
                    return corrected_response
                
                return final_response
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Tool parsing error: {e}")
                return response
        
        return response

async def main():
    """Test production agent"""
    agent = SageAgentProduction()
    
    print("🎯 PRODUCTION AGENT TEST")
    print("=" * 50)
    
    test_queries = [
        "Find recipes that contain cumin",
        "What recipes have garlic in them?", 
        "List all available recipe files",
        "Show me a recipe that uses nutritional yeast",
        "Find spicy recipes with hot peppers"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 30)
        
        response = await agent.chat(query)
        print(f"💬 Response: {response}")
        
        # Quick honesty check
        response_lower = response.lower()
        honest_indicators = ["not found", "could not find", "don't see", "none", "no recipes"]
        potentially_honest = any(indicator in response_lower for indicator in honest_indicators)
        
        print(f"🎯 Honesty indicators: {'✅' if potentially_honest else '❓'}")

if __name__ == "__main__":
    asyncio.run(main())