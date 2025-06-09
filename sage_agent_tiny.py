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
            prompt="""You are Sage, a culinary AI assistant specialized in recipe analysis and meal planning.

You have access to filesystem tools that can:
- Read recipe files from the test-recipes directory
- List recipe collections
- Analyze recipe content and structure

When users ask about recipes, use the available tools to read and analyze the files. Provide helpful insights about ingredients, techniques, dietary information, and cooking methods.

Always be thorough in your analysis and provide professional culinary insights."""
        )
        
        print("🌿 Sage Agent initialized with tiny-agents framework")
        
    async def chat(self, message: str) -> str:
        """Process a chat message through the agent"""
        if not self.agent:
            await self.initialize()
            
        # Load tools if not already loaded
        await self.agent.load_tools()
        
        # Collect all response chunks
        response_parts = []
        async for chunk in self.agent.run(message):
            if hasattr(chunk, 'content') and chunk.content:
                response_parts.append(chunk.content)
            elif isinstance(chunk, dict) and 'content' in chunk:
                response_parts.append(chunk['content'])
                
        return ''.join(response_parts) if response_parts else "No response received"
        
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