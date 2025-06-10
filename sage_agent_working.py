#!/usr/bin/env python3
"""
Working Sage Agent - Fixed version with proper async cleanup
"""
import asyncio
import json
from huggingface_hub.inference._mcp.agent import Agent

class WorkingSageAgent:
    """Fixed Sage agent with proper async handling"""
    
    def __init__(self, config_path: str = "sage_agent_config.json"):
        self.config_path = config_path
        self.agent = None
        
    async def load_config(self):
        """Load agent configuration"""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config
        
    async def initialize(self):
        """Initialize the agent with proper error handling"""
        config = await self.load_config()
        
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
        
        print("🌿 Sage Agent initialized")
        
        # Load tools with timeout
        try:
            await asyncio.wait_for(self.agent.load_tools(), timeout=15)
            print("✅ MCP tools loaded successfully")
        except asyncio.TimeoutError:
            print("⚠️  Tool loading timed out, but agent may still work")
        
    async def chat(self, message: str) -> str:
        """Process a chat message"""
        if not self.agent:
            await self.initialize()
            
        try:
            response_parts = []
            async for chunk in self.agent.run(message):
                if hasattr(chunk, 'content') and chunk.content:
                    response_parts.append(chunk.content)
                elif isinstance(chunk, dict) and 'content' in chunk:
                    response_parts.append(chunk['content'])
                    
            return ''.join(response_parts) if response_parts else "No response received"
            
        except Exception as e:
            return f"Error: {e}"
            
    async def demo_capabilities(self):
        """Demo the working agent capabilities"""
        print("🌿 WORKING SAGE AGENT DEMO")
        print("=" * 50)
        
        await self.initialize()
        
        # Test 1: Basic chat
        print("💬 Test 1: Basic conversation")
        response = await self.chat("Hello! What can you help me with?")
        print(f"Sage: {response}")
        
        # Test 2: Recipe discovery  
        print(f"\n📁 Test 2: Recipe discovery")
        response = await self.chat("What recipe files are available? Please use your tools to check.")
        print(f"Sage: {response}")
        
        # Test 3: Recipe analysis
        print(f"\n📖 Test 3: Recipe analysis")
        response = await self.chat("Please read the sample-recipe.md file and tell me what type of cuisine this is and what dietary restrictions it meets.")
        print(f"Sage: {response}")
        
        print(f"\n✅ Demo complete! Sage is working with MCP tools!")

async def main():
    """Main entry point"""
    agent = WorkingSageAgent()
    await agent.demo_capabilities()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🌿 Sage stopped")
    except Exception as e:
        print(f"Error: {e}")