#!/usr/bin/env python3
"""
Test script for google-generativeai migration.
Tests the new LLMClient implementation with Google's native SDK.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from llm_client import LLMClient


def test_client_initialization():
    """Test that the client initializes correctly."""
    print("Testing client initialization...")

    # Test without API key (should fail)
    try:
        client = LLMClient()
        print("❌ Expected error when no API key provided")
        return False
    except ValueError as e:
        if "GOOGLE_API_KEY" in str(e):
            print("✅ Correctly fails without API key")
        else:
            print(f"❌ Unexpected error: {e}")
            return False

    return True


def test_client_with_api_key():
    """Test client with API key (if provided)."""
    print("\nTesting client with API key...")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not set, skipping API test")
        print("   Set GOOGLE_API_KEY to test full functionality")
        return True

    try:
        client = LLMClient(provider="google", model="gemini-1.5-flash")
        print("✅ Client initialized successfully")

        # Test a simple call
        response = client.call_llm("Hello! How are you?")
        print(f"✅ LLM call successful")
        print(f"   Response: {response['text_response'][:100]}...")
        print(f"   Expression called: {response['expression_called']}")

        return True
    except Exception as e:
        print(f"❌ Error with API key: {e}")
        return False


def test_unsupported_provider():
    """Test that unsupported providers are rejected."""
    print("\nTesting unsupported provider rejection...")

    try:
        client = LLMClient(provider="openai")
        print("❌ Should have rejected openai provider")
        return False
    except ValueError as e:
        if "Unsupported provider" in str(e):
            print("✅ Correctly rejects unsupported provider")
        else:
            print(f"❌ Unexpected error: {e}")
            return False

    return True


def main():
    """Run all tests."""
    print("Testing google-generativeai migration...")
    print("=" * 50)

    tests = [
        test_client_initialization,
        test_unsupported_provider,
        test_client_with_api_key,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
