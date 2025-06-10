#!/usr/bin/env python3
"""
Sage Agent - Simplified version that works reliably
Uses direct API calls instead of async streaming
"""
import json
import requests
import subprocess
import asyncio

class SimpleSageAgent:
    """Simplified Sage agent with reliable LM Studio integration"""
    
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.mcp_process = None
        
    async def start_mcp_server(self):
        """Start MCP filesystem server"""
        try:
            print("🔧 Starting MCP filesystem server...")
            self.mcp_process = subprocess.Popen([
                "node", 
                "mcp-servers/src/filesystem/dist/index.js", 
                "test-recipes"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            await asyncio.sleep(1)  # Give it time to start
            print("✅ MCP server started")
            return True
        except Exception as e:
            print(f"❌ Failed to start MCP server: {e}")
            return False
            
    def call_lm_studio(self, message: str, context: str = "") -> str:
        """Direct call to LM Studio API"""
        system_prompt = f"""You are Sage, a culinary AI assistant. 
        
{context}

Provide helpful culinary insights and recipe analysis."""
        
        payload = {
            "model": "local-model",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer lm-studio"
        }
        
        try:
            response = requests.post(self.lm_studio_url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"Error: LM Studio returned {response.status_code}"
        except Exception as e:
            return f"Error calling LM Studio: {e}"
            
    def read_recipe_file(self, filename: str) -> str:
        """Read a recipe file directly"""
        try:
            with open(f"test-recipes/{filename}", 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading {filename}: {e}"
            
    def list_recipes(self) -> str:
        """List available recipe files"""
        try:
            import os
            files = os.listdir("test-recipes")
            recipe_files = [f for f in files if f.endswith('.md')]
            return f"Available recipes: {', '.join(recipe_files)}"
        except Exception as e:
            return f"Error listing recipes: {e}"
            
    def process_message(self, message: str) -> str:
        """Process user message with recipe context"""
        # Check if user is asking about recipes
        if any(word in message.lower() for word in ['recipe', 'recipes', 'list', 'files', 'available']):
            recipe_list = self.list_recipes()
            context = f"Recipe files available: {recipe_list}"
        elif 'sample' in message.lower() or 'cashew' in message.lower():
            recipe_content = self.read_recipe_file("sample-recipe.md")
            context = f"Here's the sample recipe content:\n{recipe_content}"
        else:
            context = ""
            
        return self.call_lm_studio(message, context)
        
    async def run_interactive(self):
        """Run simplified interactive mode"""
        print("🌿 Sage Agent (Simplified Mode)")
        print("Type 'quit' to exit")
        print("-" * 50)
        
        # Test LM Studio first
        test_response = self.call_lm_studio("Say hello!")
        if "Error" in test_response:
            print(f"❌ LM Studio not working: {test_response}")
            return
        print("✅ LM Studio connected")
        
        try:
            while True:
                user_input = input("\nUser: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                    
                print("Sage: ", end="", flush=True)
                response = self.process_message(user_input)
                print(response)
                
        except KeyboardInterrupt:
            print("\n🌿 Sage Agent stopped")
            
        # Cleanup
        if self.mcp_process:
            self.mcp_process.terminate()

async def main():
    """Main entry point"""
    agent = SimpleSageAgent()
    await agent.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())