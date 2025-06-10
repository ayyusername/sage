#!/usr/bin/env python3
"""
Sage Agent Accurate - Enhanced version with hallucination prevention
"""
import json
import asyncio
import os
from openai import OpenAI

class SageAgentAccurate:
    """Accuracy-focused Sage agent that prevents hallucinations"""
    
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
        
        print("🌿 Sage Agent Accurate initialized")
        print(f"✅ LM Studio: {config['base_url']}")
        
    def execute_tool(self, tool_name: str, parameters: dict) -> str:
        """Execute file operations directly"""
        
        if tool_name == "list_directory":
            path = parameters.get("path", "/Users/josh/Rose/sage/test-recipes/")
            if os.path.exists(path):
                files = os.listdir(path)
                return f"Files found: {', '.join(files)}"
            else:
                return f"Directory not found: {path}"
                
        elif tool_name == "read_file":
            path = parameters.get("path", "")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.read()
                return f"File content:\n{content}"
            else:
                return f"File not found: {path}"
                
        elif tool_name == "read_multiple_files":
            paths = parameters.get("paths", [])
            results = []
            
            for path in paths[:5]:  # Limit to 5 files
                full_path = f"/Users/josh/Rose/sage/test-recipes/{path}"
                if os.path.exists(full_path):
                    with open(full_path, 'r') as f:
                        content = f.read()
                    results.append(f"\n=== {path} ===\n{content}")
                else:
                    results.append(f"\n=== {path} === \nFile not found")
                    
            return "".join(results)
        else:
            return f"Unknown tool: {tool_name}"
    
    async def call_llm(self, messages: list) -> str:
        """Call LM Studio"""
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=messages,
                max_tokens=1000,
                temperature=0.3  # Lower temperature for more accuracy
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Error: {e}"
    
    async def extract_facts(self, tool_result: str, user_query: str) -> str:
        """Extract only factual information from tool results"""
        extraction_prompt = f"""EXTRACT ONLY FACTUAL INFORMATION from the tool results below.

Tool Results:
{tool_result}

User Query: {user_query}

RULES:
1. Only extract information that EXPLICITLY appears in the tool results
2. Do NOT add any information not present in the tool results
3. If the requested information is not found, state "NOT FOUND"
4. Be specific about what you found and what you didn't find

Extract the facts:"""

        messages = [{"role": "user", "content": extraction_prompt}]
        return await self.call_llm(messages)
    
    async def chat(self, message: str) -> str:
        """Main chat with enhanced accuracy"""
        if not self.client:
            await self.initialize()
            
        # Enhanced system prompt focused on accuracy
        system_prompt = """You are Sage, a culinary AI assistant with file access tools.

CRITICAL ACCURACY RULES:
1. ONLY use information from tool results - NEVER add information not present in tool results
2. If requested information is not in tool results, explicitly state it was not found
3. NEVER make up ingredients, cooking times, or other details
4. When tool results don't contain what the user wants, say so honestly

Tool call format:
TOOL_CALL: {"name": "tool_name", "parameters": {"param": "value"}}

Available tools:
- list_directory: {"path": "/Users/josh/Rose/sage/test-recipes/"}
- read_file: {"path": "/Users/josh/Rose/sage/test-recipes/filename.md"}  
- read_multiple_files: {"paths": ["file1.md", "file2.md"]}

Examples of HONEST responses:
- "I searched through all recipes but none contain cumin"
- "Based on the recipes I found, here are the ones that actually contain [ingredient]"
- "I couldn't find any recipes matching that criteria in the available files"

Be helpful by being truthful, not by making things up."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        # Get LLM response
        response = await self.call_llm(messages)
        
        # Check for tool calls
        if "TOOL_CALL:" in response:
            try:
                # Extract tool call
                tool_start = response.find("TOOL_CALL:") + 10
                tool_json = response[tool_start:].strip()
                
                # Find the JSON part - look for complete JSON with nested braces
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
                print(f"🔧 Executing: {tool_call_str[:50]}...")
                
                tool_call = json.loads(tool_call_str)
                tool_name = tool_call["name"]
                parameters = tool_call["parameters"]
                
                # Execute tool
                tool_result = self.execute_tool(tool_name, parameters)
                print(f"📄 Tool result length: {len(tool_result)} chars")
                
                # TWO-STAGE PROCESSING: Extract facts first, then generate response
                facts = await self.extract_facts(tool_result, message)
                print(f"📊 Extracted facts: {facts[:100]}...")
                
                # Generate final response based on extracted facts
                final_messages = [
                    {"role": "system", "content": "You are Sage. Provide a helpful response based ONLY on the factual information provided. Do not add any information not explicitly stated in the facts."},
                    {"role": "user", "content": f"User query: {message}"},
                    {"role": "user", "content": f"Factual information available: {facts}"},
                    {"role": "user", "content": "Provide a helpful response based only on these facts:"}
                ]
                
                final_response = await self.call_llm(final_messages)
                return final_response
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Tool parsing error: {e}")
                return response
        
        return response

async def main():
    """Test the accurate agent"""
    agent = SageAgentAccurate()
    
    print("🎯 Testing Accurate Agent")
    print("=" * 40)
    
    # Test the cumin search that previously hallucinated
    query = "I need recipes that contain cumin. Please search through all recipe files and tell me which ones actually contain cumin."
    print(f"Query: {query}")
    print("-" * 40)
    
    response = await agent.chat(query)
    print(f"Response: {response}")
    
    # Check if it's honest about not finding cumin
    response_lower = response.lower()
    honest = any(phrase in response_lower for phrase in [
        "no", "not found", "don't contain", "none", "couldn't find"
    ])
    
    print(f"\n🎯 Honesty check: {'✅ HONEST' if honest else '❌ STILL HALLUCINATING'}")

if __name__ == "__main__":
    asyncio.run(main())