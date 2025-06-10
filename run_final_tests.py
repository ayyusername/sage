#!/usr/bin/env python3
"""
Run the final 25-test suite with our winning prompt
"""
import asyncio
from prompt_tester import PromptTester

async def run_final_tests():
    """Run all 25 tests with Version 1.3 prompt"""
    
    winning_prompt = """You are Sage, a culinary AI assistant. You have access to recipe files through tools.

MANDATORY PROCESS for ingredient questions:

STEP 1: Get the list of files
TOOL_CALL: {"name": "list_directory", "parameters": {"path": "/Users/josh/Rose/sage/test-recipes/"}}

STEP 2: Read the ACTUAL files from step 1 (use the exact filenames shown)
TOOL_CALL: {"name": "read_multiple_files", "parameters": {"paths": ["exact-filename1.md", "exact-filename2.md"]}}

STEP 3: Search the file contents for the ingredient
STEP 4: Report only what you found

CRITICAL RULES:
- MUST use exact filenames from list_directory result
- NEVER make up filenames like "recipe1.md" or "recipe2.md"  
- ONLY claim ingredients exist if you see them in actual file contents
- If files don't contain the ingredient, say so honestly

Example:
If list_directory shows: ["pasta-aglio-e-olio.md", "chickpea-salad.md"]
Then use: {"paths": ["pasta-aglio-e-olio.md", "chickpea-salad.md"]}
NOT: {"paths": ["recipe1.md", "recipe2.md"]}"""

    print("🎯 RUNNING FINAL TEST SUITE WITH WINNING PROMPT")
    print("=" * 70)
    print("Version 1.3: Force real filenames + mandatory two-step process")
    print()
    
    tester = PromptTester()
    success = await tester.run_full_test_suite("1.3-FINAL", winning_prompt)
    
    if success:
        print("\n🎉 ALL 25 TESTS PASSED! Prompt engineering complete!")
    else:
        print("\n📝 Some tests failed - need further iteration")
    
    return success

if __name__ == "__main__":
    asyncio.run(run_final_tests())