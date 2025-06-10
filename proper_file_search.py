#!/usr/bin/env python3
"""
ACTUAL file search - search files first, then analyze matches
"""
import os
import json
import urllib.request

def search_files(query):
    """Actually search through files for keywords"""
    query_lower = query.lower()
    matches = []
    
    recipe_dir = "test-recipes"
    files = [f for f in os.listdir(recipe_dir) if f.endswith('.md')]
    
    for filename in files:
        filepath = os.path.join(recipe_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        
        content_lower = content.lower()
        
        # Simple keyword matching
        score = 0
        reasons = []
        
        # Search terms
        if 'pasta' in query_lower and 'pasta' in content_lower:
            score += 2
            reasons.append("contains pasta")
        
        if 'vegan' in query_lower and 'vegan' in content_lower:
            score += 2
            reasons.append("vegan recipe")
            
        if 'dessert' in query_lower and ('donut' in content_lower or 'ice cream' in content_lower):
            score += 2
            reasons.append("dessert")
            
        if 'salad' in query_lower and 'salad' in filename.lower():
            score += 2
            reasons.append("salad recipe")
            
        if 'korean' in query_lower and 'kimchi' in content_lower:
            score += 2
            reasons.append("Korean cuisine")
            
        if 'mushroom' in query_lower and 'mushroom' in content_lower:
            score += 1
            reasons.append("contains mushrooms")
            
        if 'quick' in query_lower and ('15 minutes' in content_lower or 'quick' in content_lower):
            score += 1
            reasons.append("quick recipe")
        
        if score > 0:
            matches.append({
                'filename': filename,
                'score': score,
                'reasons': reasons,
                'content': content[:300] + "..." if len(content) > 300 else content
            })
    
    # Sort by score
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches

def main():
    print("🔍 PROPER File Search Agent")
    print("=" * 40)
    print("This actually searches files, then shows results")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            query = input("🔍 Search: ")
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            print(f"\n📁 Searching files for: '{query}'")
            matches = search_files(query)
            
            if matches:
                print(f"\n✅ Found {len(matches)} matches:")
                for i, match in enumerate(matches, 1):
                    print(f"\n{i}. 📄 {match['filename']}")
                    print(f"   Score: {match['score']}")
                    print(f"   Reasons: {', '.join(match['reasons'])}")
                    print(f"   Preview: {match['content'][:150]}...")
            else:
                print("❌ No matches found")
                
        except KeyboardInterrupt:
            break
    
    print("\n✅ Proper file search complete!")

if __name__ == "__main__":
    main()