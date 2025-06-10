#!/usr/bin/env python3
"""
Test to verify exactly what files the agent is reading
"""
import asyncio
from sage_agent_debug import SageAgentDebug

async def test_file_reading_detailed():
    """Test what files are actually being read"""
    agent = SageAgentDebug()
    
    print("🔍 DETAILED FILE READING TEST")
    print("=" * 60)
    
    # Test 1: Olive oil search - should read files, not guess from filenames
    print("\n1️⃣ OLIVE OIL SEARCH TEST")
    print("-" * 40)
    print("This should read the actual file contents to check for 'olive oil'")
    print("NOT just guess from filename 'pasta-aglio-e-olio.md'")
    print()
    
    response = await agent.chat("Find recipes that contain olive oil")
    
    print("\n📊 ANALYSIS OF WHAT HAPPENED:")
    print("-" * 40)
    
    # Check what files were actually read
    file_reads = [log for log in agent.conversation_log if log["type"] == "FILE_READ_SUCCESS"]
    file_attempts = [log for log in agent.conversation_log if log["type"] == "FILE_READ_ATTEMPT"]
    tool_calls = [log for log in agent.conversation_log if log["type"] == "TOOL_CALL"]
    
    print(f"📁 Tool calls made: {len(tool_calls)}")
    for tool in tool_calls:
        print(f"   - {tool['content']}")
    
    print(f"🔍 File read attempts: {len(file_attempts)}")
    for attempt in file_attempts:
        print(f"   - {attempt['content']}")
    
    print(f"✅ Successful file reads: {len(file_reads)}")
    for read in file_reads:
        print(f"   - {read['content']}")
        if 'extra_data' in read and 'first_100_chars' in read['extra_data']:
            preview = read['extra_data']['first_100_chars']
            print(f"     Preview: {preview[:50]}...")
    
    print(f"\n💬 Final response: {response}")
    
    # Check if agent actually verified olive oil content
    actually_verified = len(file_reads) > 0
    print(f"\n🎯 Actually read file contents: {'✅' if actually_verified else '❌'}")
    
    if not actually_verified:
        print("❌ PROBLEM: Agent guessed from filenames without reading content!")
        print("   Solution: Agent needs to read files to verify ingredient presence")
    
    # Test 2: Let's manually check if pasta-aglio-e-olio actually contains olive oil
    print(f"\n2️⃣ MANUAL VERIFICATION")
    print("-" * 40)
    
    # Force read the file to see what it actually contains
    manual_result = agent.execute_tool("read_file", {
        "path": "/Users/josh/Rose/sage/test-recipes/pasta-aglio-e-olio.md"
    })
    
    print("📄 Contents of pasta-aglio-e-olio.md:")
    print(manual_result[:300] + "..." if len(manual_result) > 300 else manual_result)
    
    contains_olive_oil = "olive oil" in manual_result.lower()
    print(f"\n✅ Actually contains 'olive oil': {contains_olive_oil}")
    
    return actually_verified, contains_olive_oil

if __name__ == "__main__":
    asyncio.run(test_file_reading_detailed())