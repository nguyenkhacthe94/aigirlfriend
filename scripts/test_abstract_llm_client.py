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

from llm_client import (
    LLMClient,
    configure_gemini,
    get_current_provider,
    get_emotion_for_text,
    get_gemini_model_recommendation,
    get_model_string,
    get_provider_validation_error,
    is_gemini_configured,
    is_provider_available,
    validate_configuration,
    validate_provider_config,
)


def test_provider_validation():
    """Test provider validation for all supported providers."""
    print("=== Testing Provider Validation ===")

    providers = ["ollama", "google", "openai", "anthropic"]

    for provider in providers:
        is_valid = validate_provider_config(provider)
        print(f"Provider {provider}: {'✓ Valid' if is_valid else '✗ Invalid'}")
        if not is_valid:
            print(f"  Error: {get_provider_validation_error(provider)}")
    print()


def test_configuration():
    """Test current configuration validation."""
    print("=== Testing Current Configuration ===")

    provider = get_current_provider()
    print(f"Current provider: {provider}")

    try:
        model_string = get_model_string()
        print(f"Model string: {model_string}")
    except Exception as e:
        print(f"Model string error: {e}")

    is_valid = validate_configuration()
    print(f"Configuration valid: {'✓ Yes' if is_valid else '✗ No'}")

    if not is_valid:
        print(f"Error: {get_provider_validation_error(provider)}")
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

    if not validate_configuration():
        print("❌ Cannot test emotion detection - configuration invalid")
        return

    for text in test_cases:
        try:
            result = get_emotion_for_text(text)
            print(f"Text: '{text}'")
            print(f"Result: {result}")
            print()
        except Exception as e:
            print(f"❌ Error processing '{text}': {e}")
            print()


def test_provider_availability():
    """Test provider availability checks."""
    print("=== Testing Provider Availability ===")

    providers = ["ollama", "google", "openai", "anthropic"]

    for provider in providers:
        available = is_provider_available(provider)
        print(f"Provider {provider}: {'✓ Available' if available else '✗ Unavailable'}")
    print()


def test_llm_client_class():
    """Test the LLMClient class functionality."""
    print("=== Testing LLMClient Class ===")

    try:
        # Test default client
        client = LLMClient()
        print(f"Default client - Provider: {client.provider}, Model: {client.model}")

        # Test specific provider clients
        if validate_provider_config("ollama"):
            ollama_client = LLMClient(provider="ollama")
            print(f"Ollama client - Provider: {ollama_client.provider}")

        if is_gemini_configured():
            gemini_client = configure_gemini("flash")
            print(
                f"Gemini client - Provider: {gemini_client.provider}, Model: {gemini_client.model}"
            )

    except Exception as e:
        print(f"❌ LLMClient error: {e}")

    print()


def test_gemini_features():
    """Test Gemini-specific features."""
    print("=== Testing Gemini Features ===")

    print(f"Gemini configured: {'✓ Yes' if is_gemini_configured() else '✗ No'}")

    # Test model recommendations
    recommendations = {
        0.2: get_gemini_model_recommendation(0.2),
        0.4: get_gemini_model_recommendation(0.4),
        0.8: get_gemini_model_recommendation(0.8),
    }

    print("Model recommendations by latency:")
    for latency, model in recommendations.items():
        print(f"  {latency}s max: {model}")

    print()


def test_performance():
    """Test performance monitoring."""
    print("=== Testing Performance Monitoring ===")

    if not validate_configuration():
        print("❌ Cannot test performance - configuration invalid")
        return

    try:
        client = LLMClient()
        result = client.get_emotion_for_text("This is a performance test!")

        print(f"Response time: {client.last_response_time:.3f}s")
        print(
            f"Performance acceptable (<500ms): {'✓ Yes' if client.is_performance_acceptable() else '✗ No'}"
        )
        print(f"Result: {result}")

    except Exception as e:
        print(f"❌ Performance test error: {e}")

    print()


def test_backward_compatibility():
    """Test backward compatibility with existing code."""
    print("=== Testing Backward Compatibility ===")

    try:
        # This should work exactly like the old API
        result = get_emotion_for_text("Testing backward compatibility!")
        print(f"✓ get_emotion_for_text() works: {result}")

        provider = get_current_provider()
        print(f"✓ get_current_provider() works: {provider}")

        is_valid = validate_configuration()
        print(f"✓ validate_configuration() works: {is_valid}")

    except Exception as e:
        print(f"❌ Backward compatibility error: {e}")

    print()


def main():
    """Main test function."""
    print("🔬 Abstract LLM Client Test Suite")
    print("=" * 50)

    test_provider_validation()
    test_configuration()
    test_provider_availability()
    test_llm_client_class()
    test_gemini_features()
    test_backward_compatibility()

    # Only test actual LLM calls if configuration is valid
    if validate_configuration():
        test_emotion_detection()
        test_performance()
    else:
        print("⚠️  Skipping LLM tests - no valid provider configured")

    print("✅ Test suite completed")


if __name__ == "__main__":
    main()
