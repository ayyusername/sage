#!/usr/bin/env python3
"""
Quick test for olive oil case
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def quick_olive_oil_test():
    """Test just the olive oil case"""
    agent = SageAgentDebug()
    
    print("🧪 QUICK TEST: Olive Oil")
    print("=" * 40)
    
    response = await agent.chat("Find recipes that contain olive oil")
    
    # Check file reads
    file_reads = [log for log in agent.conversation_log if log.get("type") == "FILE_READ_SUCCESS"]
    tool_calls = [log for log in agent.conversation_log if log.get("type") == "TOOL_CALL"]
    
    print(f"Response: {response}")
    print(f"\n📊 Analysis:")
    print(f"Tool calls: {len(tool_calls)}")
    print(f"File reads: {len(file_reads)}")
    print(f"Issue: {'❌ No file reads' if len(file_reads) == 0 else '✅ Files read'}")
    
    return len(file_reads) > 0

if __name__ == "__main__":
    asyncio.run(quick_olive_oil_test())