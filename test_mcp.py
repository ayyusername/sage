#!/usr/bin/env python3
"""
Test MCP filesystem server communication
"""
import json
import subprocess
import asyncio

async def test_mcp_communication():
    """Test basic MCP communication with filesystem server"""
    
    # Start filesystem server
    cmd = [
        "node", 
        "mcp-servers/src/filesystem/dist/index.js",
        "test-recipes"
    ]
    
    print(f"Starting: {' '.join(cmd)}")
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Test list_directory
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "list_directory",
            "arguments": {"path": "test-recipes"}
        }
    }
    
    try:
        # Send request
        message = json.dumps(request) + "\n"
        process.stdin.write(message.encode())
        await process.stdin.drain()
        
        # Read response
        response_line = await process.stdout.readline()
        response = json.loads(response_line.decode().strip())
        
        print("Response:", json.dumps(response, indent=2))
        
        # Test read_file
        request2 = {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "read_file",
                "arguments": {"path": "test-recipes/sample-recipe.md"}
            }
        }
        
        message2 = json.dumps(request2) + "\n"
        process.stdin.write(message2.encode())
        await process.stdin.drain()
        
        response_line2 = await process.stdout.readline()
        response2 = json.loads(response_line2.decode().strip())
        
        print("File content:", json.dumps(response2, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.terminate()
        await process.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_communication())