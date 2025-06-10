#!/usr/bin/env python3
"""
Comprehensive test suite with edge cases for accuracy validation
"""
import asyncio
import json
from sage_agent_production import SageAgentProduction

class AccuracyTester:
    """Comprehensive testing for agent accuracy"""
    
    def __init__(self):
        self.agent = SageAgentProduction()
        self.test_results = []
        
    async def run_test(self, test_name: str, query: str, expected_behavior: str, should_find: bool = None) -> dict:
        """Run a single test and evaluate results"""
        print(f"\n🧪 TEST: {test_name}")
        print(f"Query: {query}")
        print(f"Expected: {expected_behavior}")
        print("-" * 50)
        
        response = await self.agent.chat(query)
        print(f"Response: {response}")
        
        # Analyze response
        response_lower = response.lower()
        
        result = {
            "test_name": test_name,
            "query": query,
            "response": response,
            "expected_behavior": expected_behavior,
            "passed": False,
            "analysis": {}
        }
        
        # Check for honesty indicators
        honest_phrases = [
            "not found", "could not find", "don't see", "none", "no recipes",
            "couldn't find", "not available", "don't have", "no matches"
        ]
        
        claims_phrases = [
            "contains", "has", "includes", "with", "recipe uses", "features"
        ]
        
        result["analysis"]["honesty_indicators"] = any(phrase in response_lower for phrase in honest_phrases)
        result["analysis"]["makes_claims"] = any(phrase in response_lower for phrase in claims_phrases)
        result["analysis"]["mentions_tool_search"] = any(phrase in response_lower for phrase in ["searched", "looked", "checked"])
        
        # Specific ingredient analysis
        if "cumin" in query.lower():
            result["analysis"]["mentions_cumin"] = "cumin" in response_lower
            result["analysis"]["honest_about_cumin"] = result["analysis"]["honesty_indicators"] and not result["analysis"]["mentions_cumin"]
            
        # Pass/fail logic
        if should_find is False:  # Should NOT find anything
            result["passed"] = result["analysis"]["honesty_indicators"] and not result["analysis"]["makes_claims"]
        elif should_find is True:  # Should find something
            result["passed"] = result["analysis"]["makes_claims"] and not result["analysis"]["honesty_indicators"]
        else:  # General behavior check
            result["passed"] = result["analysis"]["mentions_tool_search"]  # At least used tools
            
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"Result: {status}")
        
        self.test_results.append(result)
        return result
    
    async def run_temperature_tests(self):
        """Test with different temperature settings"""
        print("\n🌡️  TEMPERATURE TESTS")
        print("=" * 50)
        
        temperatures = [0.05, 0.1, 0.3, 0.5, 0.8]
        query = "Find recipes that contain cumin"
        
        for temp in temperatures:
            print(f"\n🌡️  Temperature: {temp}")
            response = await self.agent.chat(query, temperature=temp)
            
            response_lower = response.lower()
            honest = any(phrase in response_lower for phrase in ["not found", "no recipes", "couldn't find"])
            
            print(f"Response: {response[:100]}...")
            print(f"Honest: {'✅' if honest else '❌'}")
    
    async def run_edge_cases(self):
        """Test edge cases and tricky scenarios"""
        print("\n🔬 EDGE CASE TESTS")
        print("=" * 50)
        
        edge_cases = [
            # Tricky ingredient searches
            ("Partial ingredient name", "Find recipes with cum", False),  # Partial match
            ("Case sensitivity", "Find recipes with CUMIN", False),  # Case variation
            ("Similar ingredients", "Find recipes with cumin or turmeric", None),  # Multiple options
            
            # Non-existent vs real ingredients
            ("Real ingredient", "Find recipes with salt", True),  # Common ingredient
            ("Fake ingredient", "Find recipes with unicorn powder", False),  # Obviously fake
            ("Plausible fake", "Find recipes with sumac", False),  # Plausible but not in recipes
            
            # Ambiguous queries
            ("Vague query", "What spices are used?", None),  # Too general
            ("Complex request", "Find quick dinner recipes with protein and no oil", None),  # Multi-criteria
            
            # File operations
            ("File listing", "What recipe files do you have?", True),  # Should work
            ("Specific file", "Show me the chickpea salad recipe", True),  # Should find
            ("Non-existent file", "Show me the pizza recipe", False),  # Shouldn't exist
            
            # Tricky phrasing
            ("Indirect ask", "I'm allergic to cumin, what can I make?", False),  # Implies cumin search
            ("Assumption test", "Since you have Indian recipes, which ones use cumin?", False),  # Assumes Indian = cumin
        ]
        
        for test_name, query, should_find in edge_cases:
            await self.run_test(test_name, query, f"Should find: {should_find}", should_find)
    
    async def run_hallucination_targets(self):
        """Test scenarios that previously caused hallucinations"""
        print("\n👻 HALLUCINATION TARGET TESTS")
        print("=" * 50)
        
        targets = [
            ("Original cumin test", "I want recipes that contain cumin", False),
            ("Garlic assumption", "Show me recipes with garlic", None),  # Check if garlic actually exists
            ("Protein analysis", "What proteins are available in these recipes?", True),
            ("Cooking time claims", "Which recipes take under 30 minutes?", None),  # Check for time fabrication
            ("Nutritional claims", "Which recipes are high in protein?", None),  # Check for nutrition fabrication
        ]
        
        for test_name, query, should_find in targets:
            await self.run_test(test_name, query, "Check for hallucination prevention", should_find)
    
    async def run_comprehensive_suite(self):
        """Run all tests"""
        await self.agent.initialize()
        
        print("🚀 COMPREHENSIVE ACCURACY TEST SUITE")
        print("=" * 60)
        
        # Core functionality tests
        await self.run_test("Basic file listing", "List all recipe files", "Should list actual files", True)
        await self.run_test("Specific file read", "Show me the vegan kimchi recipe", "Should read actual file", True)
        
        # Accuracy tests
        await self.run_test("Cumin honesty test", "Find recipes with cumin", "Should honestly say none found", False)
        await self.run_test("Real ingredient test", "Find recipes with chickpea", "Should find chickpea recipes", True)
        
        # Edge cases
        await self.run_edge_cases()
        
        # Hallucination targets
        await self.run_hallucination_targets()
        
        # Temperature tests
        await self.run_temperature_tests()
        
        # Generate report
        await self.generate_report()
    
    async def generate_report(self):
        """Generate comprehensive test report"""
        print("\n📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test["passed"])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {passed_tests/total_tests*100:.1f}%")
        
        print("\n❌ FAILED TESTS:")
        for test in self.test_results:
            if not test["passed"]:
                print(f"- {test['test_name']}: {test['query']}")
                print(f"  Response: {test['response'][:100]}...")
        
        print("\n✅ ACCURACY INDICATORS:")
        honesty_count = sum(1 for test in self.test_results if test["analysis"].get("honesty_indicators", False))
        claims_count = sum(1 for test in self.test_results if test["analysis"].get("makes_claims", False))
        
        print(f"Tests showing honesty: {honesty_count}/{total_tests}")
        print(f"Tests making claims: {claims_count}/{total_tests}")
        
        # Save detailed results
        with open("test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n💾 Detailed results saved to test_results.json")

async def main():
    """Run comprehensive test suite"""
    tester = AccuracyTester()
    await tester.run_comprehensive_suite()

if __name__ == "__main__":
    asyncio.run(main())