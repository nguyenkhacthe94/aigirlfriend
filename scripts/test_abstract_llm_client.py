#!/usr/bin/env python3
"""
Test script for the new abstract LLM client implementation.
This script validates configuration and tests emotion detection with different providers.
"""

import json
import os
import sys

# Add project root to path so we can import llm_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from llm_client import LLMClient


def test_provider_validation():
    """Test provider validation for all supported providers."""
    print("=== Testing Provider Validation ===")

    providers = ["ollama", "google", "openai", "anthropic"]

    for provider in providers:
        try:
            client = LLMClient(provider=provider)
            print(f"Provider {provider}: ✓ Valid")
        except Exception as e:
            print(f"Provider {provider}: ✗ Invalid")
            print(f"  Error: {e}")
    print()


def test_configuration():
    """Test current configuration validation."""
    print("=== Testing Current Configuration ===")

    try:
        client = LLMClient()
        print(f"Current provider: {client.provider}")
        print(f"Current model: {client.model}")
        print("Configuration valid: ✓ Yes")
    except Exception as e:
        print("Configuration valid: ✗ No")
        print(f"Error: {e}")
    print()


def test_emotion_detection():
    """Test emotion detection functionality."""
    print("=== Testing Emotion Detection ===")

    test_cases = [
        "Wow, that's amazing news!",
        "I'm so sad about what happened.",
        "This is absolutely terrible!",
        "What a surprise!",
        "Just another normal day.",
    ]

    try:
        client = LLMClient()
    except Exception as e:
        print(f"❌ Cannot test emotion detection - configuration error: {e}")
        return

    for text in test_cases:
        try:
            result = client.call_llm(text)
            print(f"Text: '{text}'")
            print(f"Response: {result.get('text_response', 'No response')}")
            print(f"Expression: {result.get('expression_called', 'None')}")
            print()
        except Exception as e:
            print(f"❌ Error processing '{text}': {e}")
            print()


def test_provider_availability():
    """Test provider availability checks."""
    print("=== Testing Provider Availability ===")

    providers = ["ollama", "google", "openai", "anthropic"]

    for provider in providers:
        try:
            client = LLMClient(provider=provider)
            print(f"Provider {provider}: ✓ Available")
        except Exception as e:
            print(f"Provider {provider}: ✗ Unavailable - {e}")
    print()


def test_llm_client_class():
    """Test the LLMClient class functionality."""
    print("=== Testing LLMClient Class ===")

    try:
        # Test default client
        client = LLMClient()
        print(f"Default client - Provider: {client.provider}, Model: {client.model}")

        # Test Google provider if configured
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key:
            google_client = LLMClient(provider="google")
            print(
                f"Google client - Provider: {google_client.provider}, Model: {google_client.model}"
            )

    except Exception as e:
        print(f"❌ LLMClient error: {e}")

    print()


def test_performance():
    """Test performance monitoring."""
    print("=== Testing Performance Monitoring ===")

    try:
        client = LLMClient()
        result = client.call_llm("This is a performance test!")

        print(f"Response time: {client.last_response_time:.3f}s")
        print(
            f"Performance acceptable (<500ms): {'✓ Yes' if client.is_performance_acceptable() else '✗ No'}"
        )
        print(f"Response: {result.get('text_response', 'No response')}")
        print(f"Expression: {result.get('expression_called', 'None')}")

    except Exception as e:
        print(f"❌ Performance test error: {e}")

    print()


def test_backward_compatibility():
    """Test that old deprecated functions are removed and new ones exist."""
    print("=== Testing API Migration ===")

    # Test that old deprecated functions are no longer available
    old_functions = [
        "get_emotion_for_text",  # This should be removed
        "get_current_provider",
        "validate_configuration",
        "validate_provider_config",
        "get_provider_validation_error",
        "is_provider_available",
        "get_model_string",
    ]

    for func_name in old_functions:
        if hasattr(LLMClient, func_name):
            print(f"❌ {func_name} still exists as class method")
        else:
            print(f"✓ {func_name} correctly removed")

    # Test that new unified function is available
    new_functions = ["call_llm"]

    for func_name in new_functions:
        if hasattr(LLMClient, func_name):
            print(f"✓ {func_name} correctly available")
        else:
            print(f"❌ {func_name} missing from class")

    print()


def main():
    """Main test function."""
    print("🔬 Abstract LLM Client Test Suite")
    print("=" * 50)

    test_provider_validation()
    test_configuration()
    test_provider_availability()
    test_llm_client_class()
    test_backward_compatibility()

    # Only test actual LLM calls if configuration is valid
    try:
        test_client = LLMClient()
        test_emotion_detection()
        test_performance()
    except Exception as e:
        print(f"⚠️  Skipping LLM tests - configuration error: {e}")

    print("✅ Test suite completed")


if __name__ == "__main__":
    main()
