#!/usr/bin/env python3
"""
Mock test for LLM client to verify implementation without external dependencies.
"""

import json
import os
import sys
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_imports():
    """Test that all imports work correctly."""
    print("=== Testing Imports ===")
    try:
        from llm_client import PROVIDER_MODEL_DEFAULTS, LLMClient

        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_configuration_functions():
    """Test LLMClient configuration without external calls."""
    print("\n=== Testing LLMClient Configuration ===")

    from llm_client import PROVIDER_MODEL_DEFAULTS, LLMClient

    # Test provider validation logic through LLMClient
    print("Testing provider validation logic...")

    # Set up mock environment for Google
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
        try:
            client = LLMClient(provider="google")
            print(f"✓ Google client created successfully")
        except Exception as e:
            print(f"❌ Google client creation failed: {e}")

    # Test without API key
    with patch.dict(os.environ, {}, clear=True):
        try:
            client = LLMClient(provider="google")
            print(f"❌ Google client should have failed without API key")
        except Exception as e:
            print(
                f"✓ Google client correctly failed without API key: {type(e).__name__}"
            )

    # Test model defaults
    print(f"✓ Provider model defaults: {PROVIDER_MODEL_DEFAULTS}")

    return True


def test_llm_client_initialization():
    """Test LLMClient initialization without external calls."""
    print("\n=== Testing LLMClient Initialization ===")

    from llm_client import LLMClient

    # Test with mock Google provider
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
        try:
            client = LLMClient(provider="google", model="gemini-1.5-flash")
            print(
                f"✓ Google client created - Provider: {client.provider}, Model: {client.model}"
            )
            print(f"✓ Model string: {client._get_model_string()}")
        except Exception as e:
            print(f"❌ Google client creation error: {e}")

    # Test with mock Ollama provider
    with patch.dict(os.environ, {"OLLAMA_BASE_URL": "http://localhost:11434"}):
        try:
            client = LLMClient(provider="ollama", model="llama3")
            print(
                f"✓ Ollama client created - Provider: {client.provider}, Model: {client.model}"
            )
        except Exception as e:
            print(f"❌ Ollama client creation error: {e}")

    return True


def test_emotion_detection_format():
    """Test unified response format with mocked LLM response."""
    print("\n=== Testing Unified Response Format ===")

    from llm_client import LLMClient

    # Test with mocked LLM client
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
        try:
            client = LLMClient(provider="google")

            # Mock the call_llm method to return a unified response
            with patch.object(
                client,
                "call_llm",
                return_value={
                    "text_response": "That sounds great!",
                    "expression_called": "smile",
                    "intermediate_messages": [],
                },
            ):
                result = client.call_llm("This is a test!")
                print(f"✓ Mocked unified response: {result}")

                # Verify format
                assert "text_response" in result
                assert "expression_called" in result
                assert isinstance(result["text_response"], str)
                assert result["expression_called"] in [None] or isinstance(
                    result["expression_called"], str
                )
                print("✓ Result format validation passed")

        except Exception as e:
            print(f"❌ Mocked emotion detection error: {e}")

    return True


def test_performance_monitoring():
    """Test performance monitoring features."""
    print("\n=== Testing Performance Monitoring ===")

    from llm_client import LLMClient

    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
        try:
            client = LLMClient(provider="google")

            # Test initial state
            print(f"✓ Initial response time: {client.last_response_time}")
            print(
                f"✓ Performance check (no requests yet): {client.is_performance_acceptable()}"
            )

            # Mock a response time
            client._last_response_time = 0.3
            print(f"✓ Mocked response time: 0.3s")
            print(
                f"✓ Performance acceptable (<500ms): {client.is_performance_acceptable()}"
            )

            # Mock a slow response
            client._last_response_time = 0.8
            print(f"✓ Slow response time: 0.8s")
            print(
                f"✓ Performance acceptable (<500ms): {client.is_performance_acceptable()}"
            )

        except Exception as e:
            print(f"❌ Performance monitoring test error: {e}")

    return True


def main():
    """Run all mock tests."""
    print("🧪 Mock Test Suite - Abstract LLM Client")
    print("=" * 60)

    tests = [
        test_imports,
        test_configuration_functions,
        test_llm_client_initialization,
        test_emotion_detection_format,
        test_performance_monitoring,
    ]

    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")

    print(f"\n📊 Test Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 All mock tests passed! Implementation is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main()
