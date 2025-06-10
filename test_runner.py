#!/usr/bin/env python3
"""
Test Runner for File Search Agent - TDD Approach
"""
import asyncio
from sage_agent_tiny import SageAgent

class TestRunner:
    def __init__(self):
        self.agent = None
    
    async def setup(self):
        """Initialize agent once"""
        self.agent = SageAgent()
        
    async def run_test(self, test_num, query, expected_tools, success_criteria):
        """Run a single test"""
        print(f"\n{'='*60}")
        print(f"🧪 TEST {test_num}: {query}")
        print(f"{'='*60}")
        
        try:
            response = await self.agent.chat(query)
            print(f"📝 RESPONSE:\n{response}")
            
            # Basic analysis
            print(f"\n🔍 ANALYSIS:")
            print(f"Expected tools: {expected_tools}")
            print(f"Response length: {len(response)} chars")
            
            # Check for specific recipe files mentioned
            recipe_files = [
                "sample-recipe.md", "vegan-donuts.md", "vegan-caramelized-onion-dip.md",
                "vegan-kimchi.md", "vegan-beef-wellington.md", "vegan-chicken-seitan.md", 
                "chickpea-salad.md", "pasta-aglio-e-olio.md", "white-bean-salad.md",
                "italian-broccoli-salad.md"
            ]
            
            mentioned_files = []
            for file in recipe_files:
                if file in response or file.replace('-', ' ').replace('.md', '') in response.lower():
                    mentioned_files.append(file)
            
            print(f"Real files mentioned: {mentioned_files}")
            
            # Check for hallucination indicators
            fake_indicators = [
                "chocolate-chris", "raspberry-flan", "mushrooms-prawn", 
                "vegan-pasta-normanno", "mushroom-lemon-tart"
            ]
            
            hallucinations = [indicator for indicator in fake_indicators if indicator in response.lower()]
            if hallucinations:
                print(f"🚨 HALLUCINATIONS DETECTED: {hallucinations}")
            else:
                print("✅ No obvious hallucinations detected")
                
            return response, mentioned_files, hallucinations
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return None, [], []

    async def test_1_basic_file_discovery(self):
        """Test 1: Basic File Discovery"""
        query = "What recipe files do you have available?"
        expected_tools = ["list_directory"]
        
        response, mentioned_files, hallucinations = await self.run_test(
            1, query, expected_tools, 
            "Lists all 10 actual files, no hallucinations"
        )
        
        # Success criteria check
        success = True
        if len(mentioned_files) < 8:  # Should mention most/all files
            print(f"❌ FAIL: Only mentioned {len(mentioned_files)} files, expected ~10")
            success = False
        if hallucinations:
            print(f"❌ FAIL: Hallucinations detected: {hallucinations}")
            success = False
        if "No response received" in str(response):
            print(f"❌ FAIL: No proper response received")
            success = False
            
        if success:
            print("✅ TEST 1 PASSED")
        else:
            print("❌ TEST 1 FAILED")
            
        return success

    async def test_2_specific_file_content(self):
        """Test 2: Specific File Content Reading"""
        query = "Show me the ingredients in the Cashew Alfredo recipe"
        expected_tools = ["list_directory", "read_file"]
        
        response, mentioned_files, hallucinations = await self.run_test(
            2, query, expected_tools,
            "Reads sample-recipe.md and shows actual ingredients"
        )
        
        # Check for actual ingredients from Cashew Alfredo
        actual_ingredients = ["cashew", "garlic", "nutritional yeast", "lemon", "salt", "pepper"]
        found_ingredients = [ing for ing in actual_ingredients if ing in response.lower()]
        
        print(f"Actual ingredients found: {found_ingredients}")
        
        success = True
        if len(found_ingredients) < 4:  # Should find most ingredients
            print(f"❌ FAIL: Only found {len(found_ingredients)} ingredients, expected ~6")
            success = False
        if hallucinations:
            print(f"❌ FAIL: Hallucinations detected: {hallucinations}")
            success = False
        if "sample-recipe" not in response.lower() and "cashew alfredo" not in response.lower():
            print(f"❌ FAIL: Doesn't reference the correct recipe file")
            success = False
            
        if success:
            print("✅ TEST 2 PASSED")
        else:
            print("❌ TEST 2 FAILED")
            
        return success

    async def test_3_content_based_matching(self):
        """Test 3: Content-Based Recipe Matching"""
        query = "Find me vegan pasta recipes"
        expected_tools = ["list_directory", "read_file"]
        
        response, mentioned_files, hallucinations = await self.run_test(
            3, query, expected_tools,
            "Identifies pasta recipes by reading file contents"
        )
        
        # Should identify pasta recipes
        pasta_recipes = ["sample-recipe.md", "pasta-aglio-e-olio.md"]  # Cashew Alfredo is pasta sauce
        found_pasta = [recipe for recipe in pasta_recipes if any(part in response.lower() for part in recipe.replace('-', ' ').replace('.md', '').split())]
        
        print(f"Pasta recipes identified: {found_pasta}")
        
        success = True
        if len(found_pasta) < 1:
            print(f"❌ FAIL: No pasta recipes identified")
            success = False
        if hallucinations:
            print(f"❌ FAIL: Hallucinations detected: {hallucinations}")
            success = False
        if "pasta" not in response.lower():
            print(f"❌ FAIL: Response doesn't mention pasta")
            success = False
            
        if success:
            print("✅ TEST 3 PASSED")
        else:
            print("❌ TEST 3 FAILED")
            
        return success

    async def run_all_tests(self):
        """Run all tests sequentially"""
        print("🚀 Starting File Search Agent Test Suite")
        await self.setup()
        
        # Run tests 1-3 for now
        test1_pass = await self.test_1_basic_file_discovery()
        test2_pass = await self.test_2_specific_file_content()  
        test3_pass = await self.test_3_content_based_matching()
        
        print(f"\n{'='*60}")
        print("📊 TEST RESULTS SUMMARY")
        print(f"{'='*60}")
        print(f"Test 1 (Basic Discovery): {'✅ PASS' if test1_pass else '❌ FAIL'}")
        print(f"Test 2 (Content Reading): {'✅ PASS' if test2_pass else '❌ FAIL'}")
        print(f"Test 3 (Content Matching): {'✅ PASS' if test3_pass else '❌ FAIL'}")
        
        total_passed = sum([test1_pass, test2_pass, test3_pass])
        print(f"\nTotal: {total_passed}/3 tests passed")
        
        return total_passed == 3

async def main():
    runner = TestRunner()
    all_passed = await runner.run_all_tests()
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("🔧 TESTS FAILED - Need to fix issues")

if __name__ == "__main__":
    asyncio.run(main())