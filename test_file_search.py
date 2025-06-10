#!/usr/bin/env python3
"""
Simple test to see if we can do basic file search
"""
import os
import asyncio

async def test_basic_file_search():
    """Test basic file search functionality"""
    print("🔍 Testing Basic File Search Capability")
    print("=" * 50)
    
    # Test 1: Can we list recipe files?
    print("📁 Test 1: List recipe files")
    recipe_dir = "test-recipes"
    if os.path.exists(recipe_dir):
        files = os.listdir(recipe_dir)
        print(f"✅ Found {len(files)} files: {files}")
    else:
        print("❌ Recipe directory not found")
        return
    
    # Test 2: Can we read and search recipe content?
    print("\n📖 Test 2: Read and analyze recipe content")
    recipe_file = "test-recipes/sample-recipe.md"
    if os.path.exists(recipe_file):
        with open(recipe_file, 'r') as f:
            content = f.read()
        print(f"✅ Recipe content ({len(content)} chars):")
        print(content[:200] + "..." if len(content) > 200 else content)
        
        # Simple content analysis
        print("\n🔍 Content Analysis:")
        ingredients = [line for line in content.split('\n') if line.startswith('- ')]
        print(f"   - Found {len(ingredients)} ingredients")
        
        # Check for dietary keywords
        is_vegan = 'vegan' in content.lower()
        has_pasta = 'pasta' in content.lower()
        print(f"   - Vegan: {is_vegan}")
        print(f"   - Contains pasta: {has_pasta}")
        
    else:
        print("❌ Recipe file not found")
        return
    
    # Test 3: Simulate search query processing
    print("\n🎯 Test 3: Simulate search query 'Find vegan pasta recipes'")
    query = "Find vegan pasta recipes"
    
    # Simple search logic
    matches = []
    for filename in files:
        filepath = os.path.join(recipe_dir, filename)
        if filename.endswith('.md'):
            with open(filepath, 'r') as f:
                content = f.read().lower()
            
            # Check if it matches our query
            if 'vegan' in content and 'pasta' in content:
                matches.append(filename)
    
    print(f"✅ Search results for '{query}':")
    if matches:
        for match in matches:
            print(f"   📄 {match}")
    else:
        print("   No matches found")
    
    print("\n🎉 Basic file search capability working!")
    print("✅ Can list recipe files")
    print("✅ Can read recipe content") 
    print("✅ Can search by keywords")
    print("✅ Ready to test with LM Studio integration")

if __name__ == "__main__":
    asyncio.run(test_basic_file_search())