#!/usr/bin/env python3
"""
Flexible Sage Chat - Works with any directory!
"""
import asyncio
import json
import os
from sage_agent_debug import SageAgentDebug

class FlexibleSageChat:
    """Flexible chat agent that works with any recipe directory"""
    
    def __init__(self, recipe_directory="/Users/josh/ObsidianVault/recipetests/"):
        self.recipe_directory = recipe_directory
        self.agent = None
        
    async def initialize(self):
        """Initialize the agent"""
        self.agent = SageAgentDebug()
        await self.agent.initialize()
        print(f"🌿 Sage Agent ready for: {self.recipe_directory}")
        
    def create_prompt(self):
        """Create flexible prompt for any directory"""
        return f"""You are Sage, a culinary AI assistant. You have access to recipe files through tools.

MANDATORY PROCESS for ingredient questions:

STEP 1: Get the list of files
TOOL_CALL: {{"name": "list_directory", "parameters": {{"path": "{self.recipe_directory}"}}}}

STEP 2: Read the ACTUAL files from step 1 (use the exact filenames shown)
TOOL_CALL: {{"name": "read_multiple_files", "parameters": {{"paths": ["exact-filename1.md", "exact-filename2.md"], "base_path": "{self.recipe_directory}"}}}}

STEP 3: Search the file contents for the ingredient
STEP 4: Report only what you found

CRITICAL RULES:
- MUST use exact filenames from list_directory result
- NEVER make up filenames like "recipe1.md" or "recipe2.md"  
- ONLY claim ingredients exist if you see them in actual file contents
- If files don't contain the ingredient, say so honestly

Example:
If list_directory shows: ["pasta-aglio-e-olio.md", "chickpea-salad.md"]
Then use: {{"paths": ["pasta-aglio-e-olio.md", "chickpea-salad.md"], "base_path": "{self.recipe_directory}"}}"""

    async def execute_tool_calls(self, response):
        """Execute any tool calls in the response"""
        remaining = response
        tool_results = []
        
        while "TOOL_CALL:" in remaining:
            try:
                # Extract tool call JSON
                start = remaining.find("TOOL_CALL:") + 10
                json_start = remaining.find("{", start)
                
                brace_count = 0
                json_end = json_start
                for i, char in enumerate(remaining[json_start:], json_start):
                    if char == "{": brace_count += 1
                    elif char == "}": brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
                
                tool_json = remaining[json_start:json_end]
                tool_call = json.loads(tool_json)
                
                # Execute the tool
                result = self.agent.execute_tool(tool_call["name"], tool_call["parameters"])
                tool_results.append(result)
                
                print(f"🔧 Executed: {tool_call['name']}")
                print(f"📄 Result: {result[:100]}..." if len(result) > 100 else result)
                
                # Move past this tool call
                remaining = remaining[json_end:]
                
            except Exception as e:
                print(f"❌ Tool error: {e}")
                break
        
        return tool_results
    
    async def chat(self, question):
        """Chat with the agent"""
        print(f"\n💭 Processing: {question}")
        print("-" * 50)
        
        messages = [
            {"role": "system", "content": self.create_prompt()},
            {"role": "user", "content": question}
        ]
        
        # Get agent's plan
        response = await self.agent.call_llm(messages, 0.1)
        print(f"🤖 Agent plan: {response}")
        
        # Execute any tool calls
        tool_results = await self.execute_tool_calls(response)
        
        if tool_results:
            # Generate final answer based on tool results
            final_messages = [
                {"role": "system", "content": "Based on the tool results below, provide your final answer. Only mention ingredients you actually found in the file contents."},
                {"role": "user", "content": f"User asked: {question}"},
                {"role": "user", "content": f"Tool results: {' '.join(tool_results)}"},
                {"role": "user", "content": "What is your final answer?"}
            ]
            
            final_answer = await self.agent.call_llm(final_messages, 0.1)
            print(f"\n✨ Final answer: {final_answer}")
            return final_answer
        else:
            print(f"\n✨ Answer: {response}")
            return response

async def main():
    """Interactive chat with flexible directory support"""
    print("🌿 FLEXIBLE SAGE CHAT")
    print("=" * 60)
    
    # Choose your directory
    directories = {
        "1": "/Users/josh/Rose/sage/test-recipes/",
        "2": "/Users/josh/ObsidianVault/recipetests/",
        "3": "custom"
    }
    
    print("Choose recipe directory:")
    print("1. Test recipes")
    print("2. Obsidian vault")
    print("3. Custom path")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "3":
        recipe_dir = input("Enter custom path: ").strip()
    else:
        recipe_dir = directories.get(choice, directories["2"])
    
    # Verify directory exists
    if not os.path.exists(recipe_dir):
        print(f"❌ Directory not found: {recipe_dir}")
        return
    
    # Initialize chat
    chat = FlexibleSageChat(recipe_dir)
    await chat.initialize()
    
    # Show what's in the directory
    files = os.listdir(recipe_dir)
    recipe_files = [f for f in files if f.endswith('.md')]
    print(f"📁 Found {len(recipe_files)} recipe files: {', '.join(recipe_files)}")
    
    print(f"\n💬 Chat started! Type 'quit' to exit")
    print("Try asking about ingredients, recipes, or cooking methods!")
    
    # Chat loop
    while True:
        question = input(f"\n🗣️  You: ").strip()
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if question:
            await chat.chat(question)

if __name__ == "__main__":
    asyncio.run(main())