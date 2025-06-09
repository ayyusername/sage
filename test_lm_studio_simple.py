#!/usr/bin/env python3
"""
Simple test of LM Studio connectivity
"""
import requests
import json

def test_lm_studio():
    """Test basic LM Studio API connectivity"""
    url = "http://localhost:1234/v1/chat/completions"
    
    payload = {
        "model": "local-model",
        "messages": [
            {"role": "user", "content": "Hello! Please respond with 'LM Studio is working!'"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer lm-studio"
    }
    
    try:
        print("🔧 Testing LM Studio connectivity...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ LM Studio Response: {message}")
            return True
        else:
            print(f"❌ LM Studio Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    test_lm_studio()