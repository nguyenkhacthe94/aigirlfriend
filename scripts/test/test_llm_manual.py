#!/usr/bin/env python3
"""
Manual test script for LLM client module with Gemini AI.

This script allows you to:
- Test the LLM client directly without VTube Studio
- Manually input test messages
- See the response time and performance
- Test both text responses and expression function calls
- Debug configuration issues

Usage:
1. Set up your environment variables (copy .env.example to .env and fill in your API key)
2. Run: python scripts/test_llm_manual.py
"""

import os
import sys
import time
from typing import Any, Dict

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from llm_client import LLMClient
except ImportError as e:
    print(f"Error importing LLMClient: {e}")
    print("Make sure you're running this script from the project root.")
    sys.exit(1)


def load_env_file(env_path: str) -> None:
    """Load environment variables from .env file."""
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
        print(f"✓ Loaded environment from {env_path}")
    else:
        print(f"⚠️  No .env file found at {env_path}")


def check_configuration() -> bool:
    """Check if the necessary environment variables are set."""
    print("\n🔍 Checking Configuration:")

    provider = os.getenv("LLM_PROVIDER", "ollama")
    model = os.getenv("LLM_MODEL", "")

    print(f"  Provider: {provider}")
    print(f"  Model: {model}")

    if provider == "google":
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if api_key and api_key != "your_google_api_key_here":
            print(
                f"  ✓ Google API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else api_key}"
            )
            return True
        else:
            print("  ❌ Google API Key: Not set or using placeholder")
            print(
                "     Get your API key from: https://makersuite.google.com/app/apikey"
            )
            return False
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key and api_key != "your_openai_api_key_here":
            print(f"  ✓ OpenAI API Key: {api_key[:10]}...{api_key[-4:]}")
            return True
        else:
            print("  ❌ OpenAI API Key: Not set")
            return False
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if api_key and api_key != "your_anthropic_api_key_here":
            print(f"  ✓ Anthropic API Key: {api_key[:10]}...{api_key[-4:]}")
            return True
        else:
            print("  ❌ Anthropic API Key: Not set")
            return False
    elif provider == "ollama":
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        print(f"  ✓ Ollama URL: {ollama_url}")
        return True
    else:
        print(f"  ❌ Unsupported provider: {provider}")
        return False


def format_response_analysis(response: Dict[str, Any]) -> str:
    """Format the response analysis for display."""
    analysis = []

    text_resp = response.get("text_response", "")
    if text_resp:
        analysis.append(f"💬 Text Response: {text_resp}")

    expression = response.get("expression_called")
    if expression:
        analysis.append(f"😊 Expression Called: {expression}()")

    # Show intermediate messages for debugging
    intermediate = response.get("intermediate_messages", [])
    if intermediate:
        analysis.append(f"🔧 Function Calls: {len(intermediate)} intermediate messages")

    return "\n".join(analysis) if analysis else "⚠️  Empty response"


def test_basic_functionality(client: LLMClient) -> None:
    """Test basic LLM functionality with predefined test cases."""
    print("\n🧪 Testing Basic Functionality:")

    test_cases = [
        "Hello! How are you doing today?",
        "That's amazing news! I'm so excited!",
        "I'm feeling a bit sad about something that happened.",
        "Can you help me understand this concept?",
        "Wow, that's incredible!",
    ]

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n--- Test {i}/5 ---")
        print(f"Input: {test_input}")

        try:
            start_time = time.time()
            response = client.call_llm(test_input)
            response_time = time.time() - start_time

            print(format_response_analysis(response))
            print(
                f"⏱️  Response Time: {response_time:.3f}s {'✓' if response_time < 0.5 else '⚠️'}"
            )

        except Exception as e:
            print(f"❌ Error: {e}")

        print("-" * 50)


def interactive_mode(client: LLMClient) -> None:
    """Run interactive testing mode."""
    print("\n🎯 Interactive Mode")
    print("Type your messages to test the LLM client.")
    print("Commands: 'quit' to exit, 'info' for client info")
    print("=" * 60)

    while True:
        user_input = input("\n💭 Your message: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break

        if user_input.lower() == "info":
            print(f"🤖 Provider: {client.provider}")
            print(f"🎯 Model: {client.model}")
            if client.last_response_time:
                print(f"⏱️  Last Response Time: {client.last_response_time:.3f}s")
                print(f"🚀 Performance OK: {client.is_performance_acceptable()}")
            continue

        if not user_input:
            print("⚠️  Please enter a message.")
            continue

        try:
            print("🔄 Processing...")
            start_time = time.time()
            response = client.call_llm(user_input)
            response_time = time.time() - start_time

            print("\n📤 Response:")
            print(format_response_analysis(response))
            print(
                f"⏱️  Response Time: {response_time:.3f}s {'✓' if response_time < 0.5 else '⚠️ (>500ms)'}"
            )

        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main test function."""
    print("🤖 LLM Client Manual Test")
    print("=" * 40)

    # Load environment variables
    env_path = os.path.join(project_root, ".env")
    load_env_file(env_path)

    # Check configuration
    if not check_configuration():
        print("\n❌ Configuration invalid. Please:")
        print("1. Copy .env.example to .env")
        print("2. Add your API key to the .env file")
        print("3. Run this script again")
        return

    # Initialize client
    print("\n🚀 Initializing LLM Client...")
    try:
        client = LLMClient()
        print(f"✓ Client initialized with {client.provider}:{client.model}")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return

    # Run tests
    try:
        # Test basic functionality first
        test_basic_functionality(client)

        # Then go interactive
        interactive_mode(client)

    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
