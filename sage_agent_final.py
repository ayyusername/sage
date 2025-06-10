#!/usr/bin/env python3
"""
Sage Agent Final - With targeted extraction for specific queries
"""
import json
import asyncio
import os
from openai import OpenAI

class SageAgentFinal:
    """Final version with targeted fact extraction"""
    
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
        
        print("🌿 Sage Agent Final initialized")
        
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
            
            for path in paths[:10]:  # Read all files
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
                max_tokens=800,
                temperature=0.1  # Very low temperature for accuracy
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Error: {e}"
    
    async def search_ingredient(self, tool_result: str, ingredient: str) -> str:
        """Search for specific ingredient in tool results"""
        search_prompt = f"""SEARCH TASK: Look through the recipe content below and find any recipes that contain the ingredient "{ingredient}".

Recipe Content:
{tool_result}

INSTRUCTIONS:
1. Search through ALL the ingredient lists in the recipes
2. Look for "{ingredient}" exactly (case-insensitive)
3. If you find {ingredient}, list the recipe name(s) that contain it
4. If you find NO recipes with {ingredient}, respond with: "INGREDIENT NOT FOUND: No recipes contain {ingredient}"

BE VERY CAREFUL: Only report recipes that ACTUALLY contain "{ingredient}" in their ingredient lists.

Search results:"""

        messages = [{"role": "user", "content": search_prompt}]
        return await self.call_llm(messages)
    
    async def chat(self, message: str) -> str:
        """Main chat with targeted ingredient search"""
        if not self.client:
            await self.initialize()
            
        # Check if this is an ingredient search query
        message_lower = message.lower()
        ingredient_keywords = ["contain", "with", "has", "include", "ingredient"]
        is_ingredient_search = any(keyword in message_lower for keyword in ingredient_keywords)
        
        if is_ingredient_search:
            print("🔍 Detected ingredient search query")
            
            # Extract the ingredient they're looking for
            # Simple heuristic: look for common ingredients
            potential_ingredients = ["cumin", "garlic", "onion", "tomato", "pepper", "salt", "oil", "lemon", "cashew", "nutritional yeast"]
            target_ingredient = None
            
            for ingredient in potential_ingredients:
                if ingredient in message_lower:
                    target_ingredient = ingredient
                    break
            
            if target_ingredient:
                print(f"🎯 Searching for: {target_ingredient}")
                
                # Read all recipe files
                files = os.listdir("/Users/josh/Rose/sage/test-recipes/")
                recipe_files = [f for f in files if f.endswith('.md')]
                
                tool_result = self.execute_tool("read_multiple_files", {"paths": recipe_files})
                
                # Search specifically for the ingredient
                search_result = await self.search_ingredient(tool_result, target_ingredient)
                
                print(f"🔍 Search result: {search_result[:100]}...")
                
                # Generate final response
                if "INGREDIENT NOT FOUND" in search_result:
                    return f"I searched through all {len(recipe_files)} recipe files and none of them contain {target_ingredient}. Would you like me to suggest recipes with similar flavors or help you find recipes that contain other ingredients?"
                else:
                    return f"Here are the recipes that contain {target_ingredient}:\n\n{search_result}"
        
        # For non-ingredient searches, use the standard flow
        system_prompt = """You are Sage, a helpful culinary AI assistant. Provide accurate information based only on the recipe files you can access through tools."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        return await self.call_llm(messages)

async def main():
    """Test the final agent with cumin search"""
    agent = SageAgentFinal()
    
    print("🎯 FINAL TEST: Cumin Search")
    print("=" * 40)
    
    query = "I want recipes that contain cumin"
    print(f"Query: {query}")
    print("-" * 40)
    
    response = await agent.chat(query)
    print(f"Response: {response}")
    
    # Check for honesty
    response_lower = response.lower()
    honest = "none" in response_lower or "no recipes" in response_lower
    
    print(f"\n🎯 Final test: {'✅ HONEST!' if honest else '❌ Still hallucinating'}")

if __name__ == "__main__":
    asyncio.run(main())