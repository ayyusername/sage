#!/usr/bin/env python3
"""
Prompt Testing Suite - 5 tests x 5 iterations each = 25 total tests
"""
import asyncio
import json
from datetime import datetime
from sage_agent_debug import SageAgentDebug

class PromptTester:
    """Test suite for prompt iterations"""
    
    def __init__(self):
        self.test_results = []
        self.current_prompt = ""
        
    def define_tests(self):
        """Define the 5 test cases of increasing difficulty"""
        return [
            {
                "name": "Cumin False Negative",
                "query": "Find recipes that contain cumin",
                "expected": "should find NONE (honest negative)",
                "success_criteria": lambda response, logs: self.check_honest_negative(response, logs, "cumin"),
                "difficulty": 1
            },
            {
                "name": "Olive Oil True Positive", 
                "query": "Find recipes that contain olive oil",
                "expected": "should read files and find actual matches",
                "success_criteria": lambda response, logs: self.check_true_positive(response, logs, "olive oil"),
                "difficulty": 2
            },
            {
                "name": "Garlic Specificity",
                "query": "Find recipes with fresh garlic (not garlic powder)",
                "expected": "should read files and check specific form",
                "success_criteria": lambda response, logs: self.check_specificity(response, logs),
                "difficulty": 3
            },
            {
                "name": "Salt Assumption Trap",
                "query": "Find recipes that use salt",
                "expected": "should read files, not assume all recipes have salt",
                "success_criteria": lambda response, logs: self.check_no_assumption(response, logs, "salt"),
                "difficulty": 4
            },
            {
                "name": "Complex Multi-Criteria",
                "query": "Find quick recipes under 30 minutes that contain protein",
                "expected": "should read files for both time and protein info",
                "success_criteria": lambda response, logs: self.check_complex_query(response, logs),
                "difficulty": 5
            }
        ]
    
    def check_honest_negative(self, response, logs, ingredient):
        """Check if agent honestly says ingredient not found"""
        file_reads = [log for log in logs if log.get("type") == "FILE_READ_SUCCESS"]
        honest_phrases = ["not found", "could not find", "no recipes", "none", "don't have"]
        
        response_lower = response.lower()
        is_honest = any(phrase in response_lower for phrase in honest_phrases)
        claims_ingredient = ingredient in response_lower and not is_honest
        
        return {
            "passed": is_honest and not claims_ingredient,
            "file_reads": len(file_reads),
            "is_honest": is_honest,
            "claims_falsely": claims_ingredient,
            "details": f"Honest: {is_honest}, False claims: {claims_ingredient}, Files read: {len(file_reads)}"
        }
    
    def check_true_positive(self, response, logs, ingredient):
        """Check if agent reads files and finds real ingredient"""
        file_reads = [log for log in logs if log.get("type") == "FILE_READ_SUCCESS"]
        mentions_ingredient = ingredient in response.lower()
        
        # Agent should read files AND mention the ingredient
        return {
            "passed": len(file_reads) > 0 and mentions_ingredient,
            "file_reads": len(file_reads),
            "mentions_ingredient": mentions_ingredient,
            "details": f"Files read: {len(file_reads)}, Mentions ingredient: {mentions_ingredient}"
        }
    
    def check_specificity(self, response, logs):
        """Check if agent handles specific ingredient requirements"""
        file_reads = [log for log in logs if log.get("type") == "FILE_READ_SUCCESS"]
        response_lower = response.lower()
        
        # Should read files and be specific about garlic type
        mentions_fresh = "fresh garlic" in response_lower or "garlic clove" in response_lower
        avoids_powder = "garlic powder" not in response_lower or "not garlic powder" in response_lower
        
        return {
            "passed": len(file_reads) > 0 and mentions_fresh,
            "file_reads": len(file_reads),
            "specific": mentions_fresh,
            "details": f"Files read: {len(file_reads)}, Specific: {mentions_fresh}"
        }
    
    def check_no_assumption(self, response, logs, ingredient):
        """Check if agent reads files instead of assuming common ingredients"""
        file_reads = [log for log in logs if log.get("type") == "FILE_READ_SUCCESS"]
        
        # If mentions ingredient, must have read files to verify
        mentions_ingredient = ingredient in response.lower()
        if mentions_ingredient:
            return {
                "passed": len(file_reads) > 0,
                "file_reads": len(file_reads),
                "verified": len(file_reads) > 0,
                "details": f"Mentioned {ingredient}, verified by reading {len(file_reads)} files"
            }
        else:
            # If doesn't mention, that's also fine if honest
            honest_phrases = ["not found", "could not find", "no recipes"]
            is_honest = any(phrase in response.lower() for phrase in honest_phrases)
            return {
                "passed": is_honest,
                "file_reads": len(file_reads),
                "honest": is_honest,
                "details": f"Didn't mention {ingredient}, honest: {is_honest}"
            }
    
    def check_complex_query(self, response, logs):
        """Check if agent handles multi-criteria queries properly"""
        file_reads = [log for log in logs if log.get("type") == "FILE_READ_SUCCESS"]
        
        # Should read files for complex queries
        response_lower = response.lower()
        mentions_time = any(word in response_lower for word in ["minutes", "quick", "time"])
        mentions_protein = any(word in response_lower for word in ["protein", "chickpea", "bean", "seitan"])
        
        return {
            "passed": len(file_reads) > 0,
            "file_reads": len(file_reads),
            "addresses_criteria": mentions_time or mentions_protein,
            "details": f"Files read: {len(file_reads)}, Addresses criteria: {mentions_time or mentions_protein}"
        }
    
    async def run_test_iteration(self, test, iteration, prompt_version):
        """Run a single test with current prompt"""
        print(f"\n🧪 {test['name']} - Iteration {iteration + 1}")
        print(f"Query: {test['query']}")
        print(f"Expected: {test['expected']}")
        
        # Create agent with current prompt
        agent = SageAgentDebug()
        
        # Override the system prompt (we'll update this with iterations)
        agent.system_prompt_override = self.current_prompt
        
        try:
            response = await agent.chat(test['query'])
            
            # Evaluate success
            result = test['success_criteria'](response, agent.conversation_log)
            
            test_record = {
                "timestamp": datetime.now().isoformat(),
                "test_name": test['name'],
                "iteration": iteration + 1,
                "prompt_version": prompt_version,
                "query": test['query'],
                "response": response,
                "passed": result['passed'],
                "details": result,
                "log_summary": {
                    "tool_calls": len([log for log in agent.conversation_log if log.get("type") == "TOOL_CALL"]),
                    "file_reads": len([log for log in agent.conversation_log if log.get("type") == "FILE_READ_SUCCESS"]),
                    "hallucinations": len([log for log in agent.conversation_log if log.get("type") == "HALLUCINATION_DETECTED"])
                }
            }
            
            self.test_results.append(test_record)
            
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"Result: {status}")
            print(f"Details: {result['details']}")
            print(f"Response: {response[:100]}...")
            
            return result['passed']
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    async def run_full_test_suite(self, prompt_version, prompt_text):
        """Run all 5 tests, 5 times each"""
        self.current_prompt = prompt_text
        
        print(f"\n🚀 RUNNING FULL TEST SUITE - PROMPT VERSION {prompt_version}")
        print("=" * 70)
        print(f"Prompt length: {len(prompt_text)} chars")
        print(f"Target: 25 total passes (5 tests × 5 iterations each)")
        
        tests = self.define_tests()
        total_passes = 0
        total_tests = 0
        
        for test in tests:
            test_passes = 0
            print(f"\n📋 TEST: {test['name']} (Difficulty {test['difficulty']})")
            print("-" * 50)
            
            for iteration in range(5):
                passed = await self.run_test_iteration(test, iteration, prompt_version)
                if passed:
                    test_passes += 1
                total_tests += 1
                
                # Brief pause between tests
                await asyncio.sleep(0.5)
            
            total_passes += test_passes
            print(f"📊 {test['name']} Results: {test_passes}/5 passed")
        
        print(f"\n🎯 FINAL RESULTS FOR PROMPT {prompt_version}")
        print("=" * 50)
        print(f"Total Passes: {total_passes}/25")
        print(f"Success Rate: {total_passes/25*100:.1f}%")
        
        # Save detailed results
        results_file = f"test_results_v{prompt_version}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "prompt_version": prompt_version,
                "prompt_text": prompt_text,
                "total_passes": total_passes,
                "total_tests": total_tests,
                "success_rate": total_passes/total_tests,
                "detailed_results": self.test_results[-25:]  # Last 25 results
            }, f, indent=2)
        
        print(f"💾 Detailed results saved to {results_file}")
        
        return total_passes >= 25

async def main():
    """Main test runner"""
    tester = PromptTester()
    
    # Start with baseline prompt
    baseline_prompt = """You are Sage, a precise culinary AI assistant. You have access to recipe files through tools.

CRITICAL ACCURACY REQUIREMENTS:
1. ONLY state information that is EXPLICITLY present in tool results
2. NEVER add ingredients, cooking methods, or details not found in the actual file contents
3. When information is not found, say so clearly: "I could not find [X] in any of the recipe files"
4. Be helpful by being truthful, not by making assumptions
5. ALWAYS use list_directory first to see what files actually exist before trying to read them

TOOL CALL FORMAT:
TOOL_CALL: {"name": "tool_name", "parameters": {"param": "value"}}

Available tools:
- list_directory: {"path": "/Users/josh/Rose/sage/test-recipes/"} - Lists actual files
- read_file: {"path": "/Users/josh/Rose/sage/test-recipes/actual-filename.md"} - Use real filenames only
- read_multiple_files: {"paths": ["actual-file1.md", "actual-file2.md"]} - Use real filenames only

CRITICAL: Never make up filenames! Always use list_directory first to see what files actually exist."""

    success = await tester.run_full_test_suite("1.0", baseline_prompt)
    
    if success:
        print("🎉 Baseline prompt already passes all tests!")
    else:
        print("📝 Need to iterate on prompt - check promptpad.md for next steps")

if __name__ == "__main__":
    asyncio.run(main())