#!/usr/bin/env python3
"""
Simple single test to check function calling
"""

import os
import sys
import time
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


def single_test():
    load_env_file()

    from llm_client import LLMClient

    print("🔬 Single Function Calling Test")
    print("=" * 40)

    client = LLMClient(provider="google", model="models/gemini-2.5-flash")

    user_input = "I'm so happy!"
    print(f"Input: {user_input}")

    try:
        response = client.call_llm(user_input)

        print(f"Text Response: {response.get('text_response', '')}")
        print(f"Expression Called: {response.get('expression_called', 'None')}")
        print(f"Has Expression: {bool(response.get('expression_called'))}")

        if response.get("expression_called"):
            print("✅ Function calling is working!")
        else:
            print("❌ Function calling is not working")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    single_test()
