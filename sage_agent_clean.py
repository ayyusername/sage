#!/usr/bin/env python3
"""
Sage Agent Clean - Simple, working implementation
OpenAI client + manual file operations (no tiny-agents overhead)
"""
import json
import asyncio
import os
from openai import OpenAI

class SageAgentClean:
    """Clean, simple Sage agent that actually works"""
    
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
        
        print("🌿 Sage Agent Clean initialized")
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
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Error: {e}"
    
    async def chat(self, message: str) -> str:
        """Main chat with tool execution"""
        if not self.client:
            await self.initialize()
            
        system_prompt = """You are Sage, a culinary AI assistant with file access.

When users ask about recipes, respond with tool calls in this exact format:
TOOL_CALL: {"name": "tool_name", "parameters": {"param": "value"}}

Available tools:
- list_directory: {"path": "/Users/josh/Rose/sage/test-recipes/"}
- read_file: {"path": "/Users/josh/Rose/sage/test-recipes/filename.md"}  
- read_multiple_files: {"paths": ["file1.md", "file2.md"]}

Examples:
User: "What recipe files are available?"
Assistant: TOOL_CALL: {"name": "list_directory", "parameters": {"path": "/Users/josh/Rose/sage/test-recipes/"}}

User: "Show me the Cashew Alfredo recipe"
Assistant: TOOL_CALL: {"name": "read_file", "parameters": {"path": "/Users/josh/Rose/sage/test-recipes/sample-recipe.md"}}

For complex queries like "quick high protein lunch", first list files, then use read_multiple_files to analyze several recipes, then provide recommendations based on actual content.

Examples for complex analysis:
User: "I want quick high protein lunch"
Assistant: TOOL_CALL: {"name": "read_multiple_files", "parameters": {"paths": ["chickpea-salad.md", "white-bean-salad.md", "vegan-chicken-seitan.md"]}}

Then analyze the results and provide specific recommendations with reasoning."""

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
                print(f"🔍 Parsing: {tool_call_str}")
                
                tool_call = json.loads(tool_call_str)
                tool_name = tool_call["name"]
                parameters = tool_call["parameters"]
                
                print(f"🔧 Executing: {tool_name}")
                
                # Execute tool
                tool_result = self.execute_tool(tool_name, parameters)
                
                # Generate final response with tool results
                follow_up_messages = messages + [
                    {"role": "assistant", "content": response},
                    {"role": "user", "content": f"Tool result: {tool_result}\n\nBased on this information, provide a helpful response to: {message}"}
                ]
                
                final_response = await self.call_llm(follow_up_messages)
                return final_response
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Tool parsing error: {e}")
                return response
        
        return response

async def main():
    """Test the clean agent"""
    agent = SageAgentClean()
    
    print("🧪 Testing Sage Agent Clean")
    print("=" * 40)
    
    tests = [
        "What recipe files do you have available?",
        "Show me the Cashew Alfredo recipe"
    ]
    
    for test in tests:
        print(f"\nTest: {test}")
        print("-" * 30)
        response = await agent.chat(test)
        print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())