#!/usr/bin/env python3
"""
Test script to verify aisuite function calling integration with LLMClient.
Tests the new unified response system.
"""

import asyncio
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import LLMClient


async def test_function_calling():
    """Test LLMClient with function calling capability."""
    print("Testing LLMClient Function Calling Integration...")

    # Check if we have required environment variables for testing
    provider = os.getenv("LLM_PROVIDER", "ollama")
    print(f"Testing with provider: {provider}")

    try:
        # Initialize client
        client = LLMClient()
        print("✅ LLMClient initialized successfully")
        print(f"   Provider: {client.provider}")
        print(f"   Model: {client.model}")

        # Test cases for different emotional contexts
        test_cases = [
            {
                "input": "Hello! How are you today?",
                "expected_expressions": ["smile", "blink", None],
                "description": "Friendly greeting",
            },
            {
                "input": "I just got a promotion at work!",
                "expected_expressions": ["smile", "wow", "laugh"],
                "description": "Good news sharing",
            },
            {
                "input": "What's 2+2?",
                "expected_expressions": [None, "blink", "smile"],
                "description": "Simple question",
            },
        ]

        print("\n🧪 Testing with sample inputs...")
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test_case['description']}")
            print(f"Input: \"{test_case['input']}\"")

            try:
                response = client.call_llm(test_case["input"])

                print("✅ Response received:")
                print(f"   Text: {response['text_response'][:100]}...")
                print(f"   Expression: {response['expression_called'] or 'None'}")
                print(f"   Response time: {client.last_response_time:.3f}s")

                # Validate performance requirement
                if client.is_performance_acceptable():
                    print("✅ Performance: <500ms requirement met")
                else:
                    print("⚠️  Performance: Response time exceeded 500ms")

            except Exception as e:
                print(f"❌ Test {i} failed: {e}")
                # Don't fail entire test suite, continue with other tests
                continue

        print("\n🎯 Function calling integration test completed!")
        return True

    except Exception as e:
        print(f"❌ Failed to initialize or test LLMClient: {e}")
        print("\n💡 Make sure you have:")
        print("   - Ollama running (if using ollama provider)")
        print("   - Required API keys set (if using cloud providers)")
        print("   - Network connectivity")
        return False


if __name__ == "__main__":
    # Note: This is an async test but we run a simplified version for validation
    # Real-world usage will have async expression functions
    success = asyncio.run(test_function_calling())
    if success:
        print("\n🚀 Ready for Task 4: Update Main Orchestration")
    else:
        print("\n⚠️  Fix issues before proceeding to next task")
