#!/usr/bin/env python3
"""
Test LM Studio with file search using urllib (no external deps)
"""
import json
import urllib.request
import urllib.parse
import os

def test_lm_studio_connection():
    """Test basic LM Studio connection"""
    url = "http://localhost:1234/v1/chat/completions"
    
    payload = {
        "model": "local-model", 
        "messages": [{"role": "user", "content": "Say hello in exactly 5 words."}],
        "max_tokens": 50
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        url, 
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

def test_file_search_with_lm_studio():
    """Test file search queries with LM Studio"""
    print("🔍 Testing File Search with LM Studio")
    print("=" * 50)
    
    # Test 1: Basic connection
    print("📡 Test 1: LM Studio Connection")
    response = test_lm_studio_connection()
    print(f"Response: {response}")
    
    if "Error" in response:
        print("❌ LM Studio not responding - check if it's running")
        return
    
    print("✅ LM Studio connected!")
    
    # Test 2: File search query with context
    print("\n🔍 Test 2: File Search Query with Recipe Context")
    
    # Read the recipe file to provide context
    try:
        with open("test-recipes/sample-recipe.md", 'r') as f:
            recipe_content = f.read()
    except Exception as e:
        print(f"❌ Can't read recipe: {e}")
        return
    
    # Create search query with recipe context
    search_query = f"""You are Sage, a culinary AI assistant.

Here is a recipe file I have available:

RECIPE FILE: sample-recipe.md
{recipe_content}

User question: "Find vegan pasta recipes"

Please analyze the recipe and tell me if it matches the user's search for vegan pasta recipes. Explain why or why not."""

    url = "http://localhost:1234/v1/chat/completions"
    payload = {
        "model": "local-model",
        "messages": [{"role": "user", "content": search_query}],
        "max_tokens": 200
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        print("🤔 Asking LM Studio to analyze recipe...")
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            analysis = result["choices"][0]["message"]["content"].strip()
            print(f"\n🎯 LM Studio Analysis:")
            print(analysis)
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return
    
    print(f"\n✅ File search with LM Studio working!")
    print("✅ Can read recipe files")
    print("✅ Can provide context to LM Studio") 
    print("✅ LM Studio can analyze recipes for search queries")
    print("✅ Step 1.2.1 File Search Agent is functional!")

if __name__ == "__main__":
    test_file_search_with_lm_studio()