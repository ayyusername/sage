#!/usr/bin/env python3
"""
Interactive file search with LM Studio
"""
import json
import urllib.request
import urllib.parse
import os

def get_recipe_context():
    """Get all recipe files and their content"""
    recipe_dir = "test-recipes"
    context = "Available recipe files:\n\n"
    
    files = [f for f in os.listdir(recipe_dir) if f.endswith('.md')]
    
    for filename in files:
        filepath = os.path.join(recipe_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        context += f"FILE: {filename}\n{content}\n\n---\n\n"
    
    return context

def ask_lm_studio(query, context):
    """Ask LM Studio with recipe context"""
    full_prompt = f"""You are Sage, a culinary AI assistant specializing in recipe search and analysis.

{context}

User question: "{query}"

Please search through the available recipes and provide helpful information. If looking for specific types of recipes, list the matching ones and explain why they match. Be concise but informative."""

    url = "http://localhost:1234/v1/chat/completions"
    payload = {
        "model": "local-model",
        "messages": [{"role": "user", "content": full_prompt}],
        "max_tokens": 400
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("🌿 Sage Recipe Search Agent")
    print("=" * 50)
    print("Loading recipe context...")
    
    context = get_recipe_context()
    print(f"✅ Loaded {len([f for f in os.listdir('test-recipes') if f.endswith('.md')])} recipes")
    
    print("\nExample queries:")
    print("- 'Find vegan pasta recipes'")
    print("- 'What dessert recipes do you have?'")
    print("- 'Show me quick lunch ideas'")
    print("- 'Find recipes with mushrooms'")
    print("- 'What Korean recipes are available?'")
    print("\nType 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            query = input("\n🔍 Search: ")
            if query.lower() in ['quit', 'exit', 'q']:
                break
                
            print("🤔 Searching recipes...")
            response = ask_lm_studio(query, context)
            print(f"\n🌿 Sage: {response}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🌿 Thanks for using Sage Recipe Search!")

if __name__ == "__main__":
    main()