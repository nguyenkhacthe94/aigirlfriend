#!/usr/bin/env python3
"""
Debug script for testing end-to-end TTS integration with LLM responses and expressions.
This script is for development use only.

Usage:
    python scripts/debug/debug_tts_integration.py
"""
import os
import sys
import time

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from llm_client import LLMClient


def test_basic_integration():
    """Test basic TTS integration with simple LLM responses."""
    print("=== Testing Basic TTS Integration ===")

    client = LLMClient()

    print(f"TTS enabled: {client.tts_enabled}")
    print(f"TTS voice: {client.tts_voice}")

    if not client.tts_enabled:
        print("TTS is disabled. Set TTS_ENABLED=true to test.")
        return

    test_prompts = [
        "Hello, how are you?",
        "Tell me a joke",
        "What's the weather like?",
        "I'm feeling happy today!",
        "That's amazing news!",
    ]

    for i, prompt in enumerate(test_prompts):
        print(f"\nTest {i+1}: '{prompt}'")
        try:
            start_time = time.time()
            response = client.call_llm(prompt)
            end_time = time.time()

            print(f"  Response time: {end_time - start_time:.3f}s")
            print(f"  Text: {response.get('text_response', 'No text')}")
            print(f"  Expression: {response.get('expression_called', 'None')}")
            print(f"  Audio file: {response.get('audio_file', 'None')}")

            # Verify audio file exists
            audio_file = response.get("audio_file")
            if audio_file and os.path.exists(audio_file):
                size = os.path.getsize(audio_file)
                print(f"  Audio file size: {size} bytes")
            elif audio_file:
                print(f"  ✗ Audio file missing: {audio_file}")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback

            traceback.print_exc()


def test_expression_integration():
    """Test TTS integration with expression function calling."""
    print("\n=== Testing Expression + TTS Integration ===")

    client = LLMClient()

    if not client.tts_enabled:
        print("TTS is disabled. Set TTS_ENABLED=true to test.")
        return

    # Prompts designed to trigger expressions
    expression_prompts = [
        "I'm so happy to see you! This is wonderful!",  # Should trigger smile/laugh
        "I'm really sad about what happened today.",  # Should trigger sad
        "Wow, that's incredible! I can't believe it!",  # Should trigger wow
        "I'm feeling a bit shy about this...",  # Should trigger shy
        "I completely agree with your point of view.",  # Should trigger agree
        "I strongly disagree with that statement.",  # Should trigger disagree
    ]

    for i, prompt in enumerate(expression_prompts):
        print(f"\nExpression test {i+1}: '{prompt}'")
        try:
            start_time = time.time()
            response = client.call_llm(prompt)
            end_time = time.time()

            total_time = end_time - start_time
            print(f"  Total time: {total_time:.3f}s {'✓' if total_time < 0.5 else '✗'}")
            print(f"  Text: {response.get('text_response', 'No text')[:100]}...")

            expression = response.get("expression_called")
            print(f"  Expression: {expression if expression else 'None'}")

            audio_file = response.get("audio_file")
            print(
                f"  Audio: {'✓' if audio_file and os.path.exists(audio_file) else '✗'}"
            )

            if audio_file and os.path.exists(audio_file):
                print(f"  Audio file: {os.path.basename(audio_file)}")

        except Exception as e:
            print(f"  ✗ Error: {e}")


def test_performance_under_load():
    """Test TTS performance with multiple rapid requests."""
    print("\n=== Testing Performance Under Load ===")

    client = LLMClient()

    if not client.tts_enabled:
        print("TTS is disabled. Set TTS_ENABLED=true to test.")
        return

    num_requests = 5
    prompt = "This is a performance test for rapid TTS generation."

    times = []
    successful_audio = 0

    for i in range(num_requests):
        print(f"\nRequest {i+1}/{num_requests}")
        try:
            start_time = time.time()
            response = client.call_llm(prompt)
            end_time = time.time()

            duration = end_time - start_time
            times.append(duration)

            audio_file = response.get("audio_file")
            if audio_file and os.path.exists(audio_file):
                successful_audio += 1

            print(f"  Time: {duration:.3f}s")
            print(
                f"  Audio: {'✓' if audio_file and os.path.exists(audio_file) else '✗'}"
            )

        except Exception as e:
            print(f"  ✗ Error: {e}")

    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)

        print(f"\nPerformance Summary:")
        print(f"  Requests: {len(times)}/{num_requests}")
        print(f"  Successful audio: {successful_audio}/{num_requests}")
        print(f"  Average time: {avg_time:.3f}s")
        print(f"  Min time: {min_time:.3f}s")
        print(f"  Max time: {max_time:.3f}s")
        print(f"  All under 500ms: {'✓' if max_time < 0.5 else '✗'}")


def test_error_handling():
    """Test TTS error handling scenarios."""
    print("\n=== Testing Error Handling ===")

    client = LLMClient()

    # Test with empty/invalid inputs
    error_test_cases = [
        ("Empty prompt", ""),
        ("Whitespace only", "   \n   "),
        ("Very long text", "A" * 5000),  # Very long text
        ("Special characters", "🤖🎵🎶💕✨🌟"),  # Emojis and special chars
    ]

    for test_name, prompt in error_test_cases:
        print(f"\n{test_name}: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'")
        try:
            response = client.call_llm(prompt)

            text_response = response.get("text_response", "")
            audio_file = response.get("audio_file")

            print(f"  Text response: {'✓' if text_response else '✗'}")
            print(
                f"  Audio file: {'✓' if audio_file and os.path.exists(audio_file) else '✗'}"
            )

            if text_response:
                print(f"  Text length: {len(text_response)}")

        except Exception as e:
            print(f"  ✗ Error (expected in some cases): {e}")


def test_configuration_scenarios():
    """Test different TTS configuration scenarios."""
    print("\n=== Testing Configuration Scenarios ===")

    # Test with TTS disabled
    print("\nTesting with TTS disabled:")
    old_tts_enabled = os.environ.get("TTS_ENABLED")
    os.environ["TTS_ENABLED"] = "false"

    try:
        client = LLMClient()
        response = client.call_llm("Hello, this should not generate audio.")

        print(f"  TTS enabled: {client.tts_enabled}")
        print(f"  Text response: {'✓' if response.get('text_response') else '✗'}")
        print(
            f"  Audio file: {'✓' if response.get('audio_file') else '✗'} (should be ✗)"
        )

    except Exception as e:
        print(f"  Error: {e}")

    finally:
        # Restore original setting
        if old_tts_enabled is not None:
            os.environ["TTS_ENABLED"] = old_tts_enabled
        else:
            os.environ.pop("TTS_ENABLED", None)

    # Test with different voice
    print("\nTesting with different voice:")
    old_voice = os.environ.get("TTS_VOICE")
    os.environ["TTS_VOICE"] = "Puck"

    try:
        client = LLMClient()
        if client.tts_enabled:
            response = client.call_llm("Testing with a different voice.")
            audio_file = response.get("audio_file")
            print(f"  Voice: {client.tts_voice}")
            print(
                f"  Audio generated: {'✓' if audio_file and os.path.exists(audio_file) else '✗'}"
            )
        else:
            print("  TTS disabled, skipping voice test")

    except Exception as e:
        print(f"  Error: {e}")

    finally:
        # Restore original setting
        if old_voice is not None:
            os.environ["TTS_VOICE"] = old_voice
        else:
            os.environ.pop("TTS_VOICE", None)


def main():
    """Run all TTS integration debug tests."""
    print("TTS Integration Debug Script")
    print("=" * 40)

    try:
        test_basic_integration()
        test_expression_integration()
        test_performance_under_load()
        test_error_handling()
        test_configuration_scenarios()

    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 40)
    print("Integration debug tests completed")


if __name__ == "__main__":
    main()
