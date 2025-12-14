#!/usr/bin/env python3
"""
Debug script for testing TTS generation functionality in isolation.
This script is for development use only.

Usage:
    python scripts/debug/debug_tts_generation.py
"""
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from llm_client import LLMClient


def test_tts_basic():
    """Test basic TTS generation with different text inputs."""
    print("=== Testing Basic TTS Generation ===")

    client = LLMClient()

    if not client.tts_enabled:
        print("TTS is disabled. Set TTS_ENABLED=true to test.")
        return

    test_texts = [
        "Hello, this is a simple test.",
        "How are you doing today? I hope you're having a wonderful time!",
        "Testing emotional expressions with excitement and joy!",
        "This is a longer sentence to test how the text-to-speech handles more complex content with multiple clauses and punctuation marks.",
        "Short.",
        "",  # Empty text
    ]

    for i, text in enumerate(test_texts):
        print(f"\nTest {i+1}: '{text}'")
        try:
            audio_file = client.generate_tts_audio(text)
            if audio_file:
                print(f"  ✓ Generated: {audio_file}")
                # Check if file exists
                if os.path.exists(audio_file):
                    file_size = os.path.getsize(audio_file)
                    print(f"  ✓ File size: {file_size} bytes")
                else:
                    print(f"  ✗ File not found: {audio_file}")
            else:
                print("  ✗ No audio file generated")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def test_tts_voices():
    """Test TTS generation with different voices."""
    print("\n=== Testing Different Voices ===")

    client = LLMClient()

    if not client.tts_enabled:
        print("TTS is disabled. Set TTS_ENABLED=true to test.")
        return

    # Common voice names from Gemini TTS documentation
    voices = ["Kore", "Puck", "Charon", "Zephyr", "Fenrir", "Leda"]
    test_text = "Hello, this is a test with different voices."

    for voice in voices:
        print(f"\nTesting voice: {voice}")
        try:
            audio_file = client.generate_tts_audio(test_text, voice=voice)
            if audio_file:
                print(f"  ✓ Generated with {voice}: {audio_file}")
            else:
                print(f"  ✗ Failed to generate with {voice}")
        except Exception as e:
            print(f"  ✗ Error with {voice}: {e}")


def test_tts_performance():
    """Test TTS generation performance and timing."""
    print("\n=== Testing TTS Performance ===")

    client = LLMClient()

    if not client.tts_enabled:
        print("TTS is disabled. Set TTS_ENABLED=true to test.")
        return

    import time

    test_text = "This is a performance test for text-to-speech generation."
    iterations = 3

    times = []
    for i in range(iterations):
        print(f"\nIteration {i+1}/{iterations}")
        start_time = time.time()

        try:
            audio_file = client.generate_tts_audio(test_text)
            end_time = time.time()
            duration = end_time - start_time
            times.append(duration)

            print(f"  Duration: {duration:.3f}s")
            if audio_file:
                print(f"  Generated: {os.path.basename(audio_file)}")
            else:
                print("  No audio file generated")
        except Exception as e:
            print(f"  Error: {e}")

    if times:
        avg_time = sum(times) / len(times)
        print(f"\nAverage generation time: {avg_time:.3f}s")
        print(f"Performance acceptable (<0.5s): {'✓' if avg_time < 0.5 else '✗'}")


def test_tts_file_management():
    """Test TTS file cleanup and management."""
    print("\n=== Testing File Management ===")

    client = LLMClient()

    print(f"TTS enabled: {client.tts_enabled}")
    print(f"TTS voice: {client.tts_voice}")

    # Test cleanup function
    try:
        cleanup_count = client.cleanup_old_audio_files()
        print(f"Cleaned up files: {cleanup_count}")
    except Exception as e:
        print(f"Cleanup error: {e}")

    # Check audio directory
    audio_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "audio"
    )
    if os.path.exists(audio_dir):
        files = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]
        print(f"Audio files in directory: {len(files)}")
        if files:
            print("Recent files:")
            for f in sorted(files)[-5:]:  # Show last 5 files
                file_path = os.path.join(audio_dir, f)
                size = os.path.getsize(file_path)
                print(f"  {f} ({size} bytes)")
    else:
        print("Audio directory does not exist")


def main():
    """Run all TTS debug tests."""
    print("TTS Generation Debug Script")
    print("=" * 40)

    try:
        test_tts_basic()
        test_tts_voices()
        test_tts_performance()
        test_tts_file_management()

    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 40)
    print("Debug tests completed")


if __name__ == "__main__":
    main()
