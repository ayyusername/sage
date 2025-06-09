#!/usr/bin/env python3
"""
Sage Agent - Simple orchestrator for MCP servers and LM Studio
"""
import json
import requests
import subprocess
import asyncio
import os
import sys
from typing import Dict, List, Any, Optional
from openai import OpenAI

class LMStudioClient:
    """Client for LM Studio's OpenAI-compatible API"""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        self.client = OpenAI(
            base_url=base_url,
            api_key="lm-studio"  # LM Studio doesn't require real key
        )
        
    def chat_completion(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict:
        """Send chat completion request to LM Studio"""
        try:
            kwargs = {
                "model": "local-model",  # LM Studio will use loaded model
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"
                
            response = self.client.chat.completions.create(**kwargs)
            return response
        except Exception as e:
            print(f"Error calling LM Studio: {e}")
            return None

class MCPClient:
    """Client for MCP server communication"""
    
    def __init__(self, server_command: List[str], server_args: List[str]):
        self.server_command = server_command
        self.server_args = server_args
        self.process = None
        
    async def start_server(self):
        """Start the MCP server process"""
        cmd = self.server_command + self.server_args
        print(f"Starting MCP server: {' '.join(cmd)}")
        
        try:
            self.process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            print("MCP server started successfully")
        except Exception as e:
            print(f"Error starting MCP server: {e}")
            
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict:
        """Call a tool on the MCP server"""
        if not self.process:
            await self.start_server()
            
        # MCP protocol message
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": parameters
            }
        }
        
        try:
            # Send request
            message = json.dumps(request) + "\n"
            self.process.stdin.write(message.encode())
            await self.process.stdin.drain()
            
            # Read response
            response_line = await self.process.stdout.readline()
            response = json.loads(response_line.decode().strip())
            
            return response
        except Exception as e:
            print(f"Error calling MCP tool {tool_name}: {e}")
            return {"error": str(e)}
            
    async def stop_server(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            await self.process.wait()

class SageAgent:
    """Main orchestrator agent"""
    
    def __init__(self):
        self.lm_client = LMStudioClient()
        self.mcp_servers = {}
        
        # Initialize File System MCP Server
        filesystem_server_path = "/Users/josh/Rose/sage/mcp-servers/src/filesystem/dist/index.js"
        allowed_dirs = ["/Users/josh/Rose/sage/test-recipes"]
        
        self.mcp_servers["filesystem"] = MCPClient(
            server_command=["node", filesystem_server_path],
            server_args=allowed_dirs
        )
        
    async def start(self):
        """Start all MCP servers"""
        for name, server in self.mcp_servers.items():
            print(f"Starting {name} MCP server...")
            await server.start_server()
            
    async def stop(self):
        """Stop all MCP servers"""
        for server in self.mcp_servers.values():
            await server.stop_server()
            
    def get_available_tools(self) -> List[Dict]:
        """Define available tools for LM Studio"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the file to read"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "list_directory",
                    "description": "List contents of a directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the directory to list"
                            }
                        },
                        "required": ["path"]
                    }
                }
            }
        ]
        
    async def execute_tool_call(self, tool_call: Dict) -> str:
        """Execute a tool call on appropriate MCP server"""
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])
        
        # Route to appropriate MCP server
        if function_name in ["read_file", "write_file", "list_directory", "create_directory"]:
            server = self.mcp_servers["filesystem"]
        else:
            return f"Unknown tool: {function_name}"
            
        result = await server.call_tool(function_name, arguments)
        
        if "error" in result:
            return f"Error: {result['error']}"
        else:
            return json.dumps(result.get("result", result), indent=2)
            
    async def process_user_message(self, user_message: str) -> str:
        """Process user message through LM Studio and MCP tools"""
        messages = [
            {
                "role": "system", 
                "content": "You are Sage, a culinary AI assistant. You can read and analyze recipe files using the available tools. When asked about recipes, use the tools to read files and provide helpful analysis."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        tools = self.get_available_tools()
        
        # Call LM Studio
        print("Calling LM Studio...")
        response = self.lm_client.chat_completion(messages, tools)
        
        if not response:
            return "Error: Could not get response from LM Studio"
            
        message = response.choices[0].message
        
        # Check if model wants to use tools
        if hasattr(message, 'tool_calls') and message.tool_calls:
            print(f"Executing {len(message.tool_calls)} tool calls...")
            
            tool_results = []
            for tool_call in message.tool_calls:
                result = await self.execute_tool_call(tool_call)
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": result
                })
                
            # Send tool results back to LM Studio
            messages.append(message)
            messages.extend(tool_results)
            
            final_response = self.lm_client.chat_completion(messages)
            if final_response:
                return final_response.choices[0].message.content
            else:
                return "Error: Could not get final response from LM Studio"
        else:
            return message.content
            
    async def run_interactive(self):
        """Run interactive CLI loop"""
        print("🌿 Sage Agent Started")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        await self.start()
        
        try:
            while True:
                user_input = input("\nUser: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                    
                response = await self.process_user_message(user_input)
                print(f"\nSage: {response}")
                
        finally:
            await self.stop()
            print("\n🌿 Sage Agent Stopped")

async def main():
    """Main entry point"""
    agent = SageAgent()
    await agent.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())