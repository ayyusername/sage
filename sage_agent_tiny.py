#!/usr/bin/env python3
"""
Sage Agent - Using Hugging Face tiny-agents with MCP
"""
import json
import asyncio
from huggingface_hub.inference._mcp.agent import Agent
from huggingface_hub import MCPClient

class SageAgent:
    """Sage culinary AI agent using tiny-agents framework"""
    
    def __init__(self, config_path: str = "sage_agent_config.json"):
        self.config_path = config_path
        self.agent = None
        
    async def load_config(self):
        """Load agent configuration"""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config
        
    async def initialize(self):
        """Initialize the tiny-agents powered agent"""
        config = await self.load_config()
        
        # Initialize agent with LM Studio configuration
        self.agent = Agent(
            model=config["model"],
            base_url=config["base_url"],
            api_key=config["api_key"],
            servers=[server_config for server_config in config.get("servers", [])],
            prompt="""You are Sage, a culinary AI assistant with file access tools.

For recipe questions, follow these patterns:
1. Specific recipe ingredients (like "Cashew Alfredo ingredients"): call read_file with the recipe path
2. "What recipes are available": call list_directory on /Users/josh/Rose/sage/test-recipes  
3. Recipe search (like "find pasta recipes"): call list_directory first, then read_file on relevant files
4. Complex analysis (like "quick lunch with protein"): 
   - First call list_directory to see all options
   - Then call read_file individually on 3-5 relevant recipes to analyze ingredients, prep time, etc.
   - Use multiple separate read_file calls, not read_multiple_files
   - Compare and recommend based on the user's criteria from actual recipe content

Recipe locations:
- Cashew Alfredo: /Users/josh/Rose/sage/test-recipes/sample-recipe.md
- All recipes: /Users/josh/Rose/sage/test-recipes/

For complex queries, read multiple recipe files to analyze and compare ingredients, preparation time, and nutritional content. Always end with clear recommendations like "I recommend [Recipe Name] because [specific reasons from the recipe content]"."""
        )
        
        print("🌿 Sage Agent initialized with tiny-agents framework")
        
    async def execute_tool(self, tool_name: str, parameters: dict) -> str:
        """Execute a tool manually"""
        import os
        
        if tool_name == "list_directory":
            path = parameters.get("path", "")
            if os.path.exists(path):
                files = os.listdir(path)
                return f"Files in {os.path.basename(path)}: {', '.join(files)}"
            else:
                return f"Directory {path} not found"
                
        elif tool_name == "read_file":
            path = parameters.get("path", "")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.read()
                return f"Content of {os.path.basename(path)}:\n{content}"
            else:
                return f"File {path} not found"
                
        elif tool_name == "read_multiple_files":
            paths = parameters.get("paths", [])
            # Handle paths that might be a string representation of a list
            if isinstance(paths, str):
                # Parse string like "['file1.md', 'file2.md']"
                try:
                    import ast
                    paths = ast.literal_eval(paths)
                except:
                    paths = [paths]  # Fallback to single file
            
            results = []
            for path in paths[:5]:  # Limit to first 5 files
                full_path = f"/Users/josh/Rose/sage/test-recipes/{path}"
                if os.path.exists(full_path):
                    with open(full_path, 'r') as f:
                        content = f.read()
                    results.append(f"\n📖 {path}:\n{content}")
                else:
                    results.append(f"\n❌ {path}: Not found")
            
            return "".join(results)
        else:
            return f"Unknown tool: {tool_name}"
    
    async def chat(self, message: str) -> str:
        """Process a chat message with manual tool execution"""
        if not self.agent:
            await self.initialize()
            
        # Load tools if not already loaded
        await self.agent.load_tools()
        
        # Get the model response
        full_response = ""
        finish_reason = None
        
        async for chunk in self.agent.run(message):
            if hasattr(chunk, 'choices') and chunk.choices:
                choice = chunk.choices[0]
                if hasattr(choice, 'delta') and choice.delta:
                    if choice.delta.content:
                        full_response += choice.delta.content
                    if choice.finish_reason:
                        finish_reason = choice.finish_reason
        
        # Check if the model wants to call a tool
        if full_response.strip().startswith('{') and 'function' in full_response:
            try:
                import json
                tool_call = json.loads(full_response.strip())
                tool_name = tool_call.get("name")
                parameters = tool_call.get("parameters", {})
                
                # Execute the tool
                tool_result = await self.execute_tool(tool_name, parameters)
                
                # Generate a follow-up response with the tool result
                follow_up = f"Based on the tool result: {tool_result}\n\nProvide a helpful response to the user's original question: {message}"
                
                final_response = ""
                async for chunk in self.agent.run(follow_up):
                    if hasattr(chunk, 'choices') and chunk.choices:
                        choice = chunk.choices[0]
                        if hasattr(choice, 'delta') and choice.delta and choice.delta.content:
                            final_response += choice.delta.content
                
                return final_response if final_response else tool_result
                
            except (json.JSONDecodeError, KeyError):
                pass
        
        return full_response if full_response else "No response received"
        
    async def run_interactive(self):
        """Run interactive chat loop"""
        print("🌿 Sage Agent (Tiny-Agents Powered)")
        print("Type 'quit' to exit")
        print("-" * 50)
        
        await self.initialize()
        
        try:
            while True:
                user_input = input("\nUser: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                    
                print("Sage: ", end="", flush=True)
                response = await self.chat(user_input)
                print(response)
                
        except KeyboardInterrupt:
            print("\n🌿 Sage Agent stopped")
        except Exception as e:
            print(f"Error: {e}")
            
    async def test_functionality(self):
        """Test basic agent functionality"""
        print("🔧 Testing Sage Agent with tiny-agents...")
        
        await self.initialize()
        
        # Test 1: List recipes
        print("\n📁 Test 1: List available recipes")
        response1 = await self.chat("What recipe files are available?")
        print(f"Response: {response1}")
        
        # Test 2: Read a recipe
        print("\n📖 Test 2: Read the sample recipe")
        response2 = await self.chat("Please read the sample-recipe.md file and tell me about it")
        print(f"Response: {response2}")
        
        print("\n✅ Testing complete!")

async def main():
    """Main entry point"""
    agent = SageAgent()
    
    # Uncomment to run tests
    # await agent.test_functionality()
    
    # Run interactive mode
    await agent.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())