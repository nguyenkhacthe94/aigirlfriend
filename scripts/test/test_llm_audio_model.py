"""
Test script to demonstrate LLM controlling both model expressions and audio playback.
This simulates:
1. LLM generates a response
2. Calls expression function (model control)
3. Generates TTS audio
4. Audio player automatically picks up and plays the audio
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from llm_client import LLMClient


async def test_llm_with_audio_and_model():
    print("=" * 70)
    print("LLM + Audio + Model Control Integration Test")
    print("=" * 70)
    print()

    # Initialize LLM client
    print("1. Initializing LLM Client...")
    try:
        llm_client = LLMClient()
        print(f"   ✓ Provider: {llm_client.provider}")
        print(f"   ✓ Model: {llm_client.model}")
        print(f"   ✓ TTS Enabled: {llm_client.tts_enabled}")
        print(f"   ✓ TTS Voice: {llm_client.tts_voice}")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        return

    # Start audio player
    print("\n2. Starting Audio Player...")
    await llm_client.start_audio_player()
    print("   ✓ Audio player is now monitoring /audio directory")

    # Wait for audio player to initialize
    await asyncio.sleep(1)

    # Test prompts that should trigger expressions
    test_prompts = [
        "That's hilarious!",  # Should trigger laugh expression
        "I love you!",        # Should trigger love expression
        "That's amazing!",    # Should trigger wow expression
    ]

    print("\n3. Testing LLM Responses with Expression + Audio...")
    print("-" * 70)

    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n[Test {i}] User: {prompt}")
        print("-" * 70)

        try:
            # Get response from LLM (this will call expression + generate TTS)
            response = llm_client.call_llm(prompt)

            print(f"🤖 AI Response: {response['text_response']}")

            if response['expression_called']:
                print(f"😊 Expression Called: {response['expression_called']}()")
            else:
                print("😐 Expression: None")

            if response.get('audio_file'):
                print(f"🔊 TTS Audio Generated: {os.path.basename(response['audio_file'])}")
                print(f"   📂 Saved to: {response['audio_file']}")
                print(f"   ⏳ Audio player will auto-detect and play...")
            else:
                print("🔇 No audio generated")

            # Give time for audio to be detected and played
            print("   ⏸️  Waiting for audio playback to complete...")
            await asyncio.sleep(5)  # Adjust based on expected audio length

            print("   ✓ Completed")

        except Exception as e:
            print(f"   ✗ Error: {e}")
            import traceback
            traceback.print_exc()

        print()

    # Check if any audio files remain
    print("\n4. Checking Audio Directory...")
    remaining_files = llm_client.audio_player.api.get_audio_list()
    if remaining_files:
        print(f"   ⚠️  {len(remaining_files)} file(s) still in queue:")
        for f in remaining_files:
            print(f"      - {f}")
        print("   Waiting for playback to complete...")
        await asyncio.sleep(10)
    else:
        print("   ✓ All audio files played and deleted")

    # Cleanup
    print("\n5. Shutting Down...")
    await llm_client.stop_audio_player()
    print("   ✓ Audio player stopped")

    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_llm_with_audio_and_model())
