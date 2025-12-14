"""
Simple test to verify audio files are deleted after playing in main.py context.
This simulates TTS audio generation without actually calling the LLM API.
"""
import asyncio
import sys
import os
import wave
import struct
import math
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from audio_player.audioPlayer import AudioPlayer


def create_tts_audio_file(text):
    """Simulate TTS by creating a simple audio file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"response_{timestamp}.wav"
    audio_dir = os.path.join(os.getcwd(), "audio")
    filepath = os.path.join(audio_dir, filename)

    # Create a short beep (simulating TTS)
    sample_rate = 24000  # Same as Gemini TTS
    duration = 1  # 1 second
    frequency = 440  # A note

    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        num_frames = int(sample_rate * duration)
        for i in range(num_frames):
            value = int(32767.0 * 0.3 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            wav_file.writeframes(struct.pack('h', value))

    print(f"Generated TTS audio: {filename}")
    return filepath


async def main():
    print("=" * 70)
    print("Main.py Audio Deletion Test")
    print("Simulates LLM generating TTS audio and audio player deleting it")
    print("=" * 70)
    print()

    # Initialize audio player (like in main.py)
    print("1. Starting Audio Player...")
    audio_player = AudioPlayer()
    audio_task = asyncio.create_task(audio_player.run())
    await asyncio.sleep(1)  # Let it initialize

    print("\n2. Simulating LLM Responses with TTS...")
    print("-" * 70)

    # Simulate 3 LLM responses
    for i in range(3):
        print(f"\n[Response {i+1}]")
        print(f"  User: Test message {i+1}")
        print(f"  AI: Generating response...")

        # Simulate TTS generation (like llm_client.generate_tts_audio())
        audio_file = create_tts_audio_file(f"Response {i+1}")
        print(f"  TTS saved to: {os.path.basename(audio_file)}")

        # Wait a bit before next response
        await asyncio.sleep(2)

    print("\n3. Waiting for all audio to play and be deleted...")
    await asyncio.sleep(5)

    # Check remaining files
    remaining = audio_player.api.get_audio_list()
    print(f"\n4. Final Check:")
    print(f"   Files remaining: {len(remaining)}")

    if remaining:
        print(f"   [WARNING] {len(remaining)} file(s) not deleted:")
        for f in remaining:
            print(f"      - {f}")
    else:
        print(f"   [SUCCESS] All audio files played and deleted!")

    # Cleanup
    print("\n5. Shutting down...")
    audio_player.stop()
    await audio_task

    print("\n" + "=" * 70)
    print("Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
