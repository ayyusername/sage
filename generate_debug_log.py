#!/usr/bin/env python3
"""
Generate a fresh debug log for browser viewing
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def generate_fresh_log():
    """Generate a debug log showing the file reading issue"""
    agent = SageAgentDebug()
    
    print("🔍 Generating fresh debug log...")
    
    # Test the problematic olive oil query
    response = await agent.chat("Find recipes that contain olive oil")
    
    # Save the log
    log_file = agent.save_debug_log("latest_debug.json")
    
    print(f"✅ Debug log saved: {log_file}")
    print(f"📄 Response was: {response[:100]}...")
    
    # Quick analysis
    file_reads = [log for log in agent.conversation_log if log["type"] == "FILE_READ_SUCCESS"]
    tool_calls = [log for log in agent.conversation_log if log["type"] == "TOOL_CALL"]
    
    print(f"\n📊 Quick Analysis:")
    print(f"   Tool calls: {len(tool_calls)}")
    print(f"   File reads: {len(file_reads)}")
    print(f"   Issue: {'❌ Agent guessed without reading files' if len(file_reads) == 0 else '✅ Agent read files'}")

if __name__ == "__main__":
    asyncio.run(generate_fresh_log())