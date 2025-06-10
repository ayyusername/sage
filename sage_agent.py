#!/usr/bin/env python3
"""
Sage Agent - Clean Direct Implementation
"""
import json
import asyncio
import subprocess
import os
from openai import OpenAI

class SageAgent:
    """Clean culinary AI agent using direct file operations"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"
        )
        self.recipes_dir = "/Users/josh/Rose/sage/test-recipes"
        
    def list_directory(self, path: str = None) -> str:
        """List files in directory"""
        target_path = path or self.recipes_dir
        try:
            if os.path.exists(target_path):
                files = os.listdir(target_path)
                return f"Files in {os.path.basename(target_path)}: {', '.join(files)}"
            else:
                return f"Directory {target_path} not found"
        except Exception as e:
            return f"Error listing directory: {e}"
            
    def read_file(self, path: str) -> str:
        """Read file contents"""
        try:
            # Handle relative paths
            if not path.startswith('/'):
                full_path = os.path.join(self.recipes_dir, path)
            else:
                full_path = path
                
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    content = f.read()
                return f"Content of {os.path.basename(full_path)}:\n{content}"
            else:
                return f"File {full_path} not found"
        except Exception as e:
            return f"Error reading file: {e}"
            
    async def chat(self, message: str) -> str:
        """Process chat message with automatic tool calling"""
        
        # Always gather file information for ANY query
        message_lower = message.lower()
        tool_results = []
        
        # Always list directory for recipe-related queries
        dir_result = self.list_directory()
        tool_results.append(f"Directory listing: {dir_result}")
        
        # Always read sample recipe for comprehensive context
        file_result = self.read_file("sample-recipe.md")
        tool_results.append(f"Sample recipe: {file_result}")
            
        context = f"\n\nTool Results:\n" + "\n".join(tool_results)
            
        system_prompt = """You are Sage, a culinary AI assistant. 

CRITICAL RULES:
1. ONLY use information from the Tool Results section below
2. NEVER invent, make up, or hallucinate any recipes or ingredients
3. If the user asks about recipes not in the Tool Results, say "I only have access to the sample-recipe.md file"
4. For ingredient matching, ONLY check the actual ingredients listed in the sample recipe
5. Be honest about limitations - don't create content that doesn't exist in the files

The only recipe data you have access to is shown in the Tool Results below."""

        try:
            response = self.client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{message}{context}"}
                ]
            )
            
            return response.choices[0].message.content
                
        except Exception as e:
            return f"Error: {e}"
            
    async def cleanup(self):
        """Clean up resources"""
        pass  # No resources to clean up with direct file operations
            
    async def run_interactive(self):
        """Run interactive chat loop"""
        print("🌿 Sage Agent (Clean Direct Implementation)")
        print("Type 'quit' to exit")
        print("-" * 50)
        
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
        finally:
            await self.cleanup()

async def main():
    """Main entry point"""
    agent = SageAgent()
    await agent.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())