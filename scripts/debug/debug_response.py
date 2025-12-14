#!/usr/bin/env python3
"""
Debug script to inspect the response from google-generativeai
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def load_env_file():
    """Load environment variables from .env file in project root."""
    env_path = project_root / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

def debug_response():
    load_env_file()
    
    from llm_client import LLMClient
    from model_control.vts_expressions import smile
    
    print("🔍 Debugging LLM Response Structure")
    print("=" * 50)
    
    client = LLMClient(provider="google", model="models/gemini-2.5-flash")
    
    # Test with a simple happy message
    user_input = "I'm so happy!"
    print(f"Input: {user_input}")
    
    # Make the raw call to see the response structure
    try:
        from google.genai import types
        response = client._client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"You are a friendly AI assistant. When users express emotions, call the appropriate expression function.\n\nUser: {user_input}",
            config=types.GenerateContentConfig(
                tools=[smile],  # Just test with one function
                temperature=0.75,
                max_output_tokens=300,
            ),
        )
        
        print("\n📋 Raw Response Attributes:")
        for attr in dir(response):
            if not attr.startswith('_'):
                try:
                    value = getattr(response, attr)
                    print(f"  {attr}: {value}")
                except:
                    print(f"  {attr}: <error accessing>")
                    
        print(f"\n📝 Response Text: {response.text}")
        print(f"📋 Has function_calls attr: {hasattr(response, 'function_calls')}")
        
        if hasattr(response, 'function_calls'):
            print(f"📋 Function calls: {response.function_calls}")
        
        print(f"📋 Has candidates attr: {hasattr(response, 'candidates')}")
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            print(f"📋 Candidate attributes:")
            for attr in dir(candidate):
                if not attr.startswith('_'):
                    try:
                        value = getattr(candidate, attr)
                        print(f"  {attr}: {value}")
                    except:
                        print(f"  {attr}: <error accessing>")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_response()