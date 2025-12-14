"""
Test script that simulates downloading audio files to the /audio directory.
The AudioPlayer should automatically:
1. Detect new .wav files
2. Play them
3. Delete them after playback
"""
import asyncio
import sys
import os
import wave
import struct
import math

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from audio_player.audioPlayer import AudioPlayer


def create_test_audio_file(filename, duration=2, frequency=440):
    """Create a simple test WAV file with a sine wave tone"""
    audio_dir = os.path.join(os.getcwd(), "audio")
    filepath = os.path.join(audio_dir, filename)

    sample_rate = 44100
    num_channels = 2
    sample_width = 2  # 16-bit

    num_frames = int(sample_rate * duration)

    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)

        # Generate sine wave
        for i in range(num_frames):
            value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            packed_value = struct.pack('h', value)
            # Write for both channels
            wav_file.writeframes(packed_value * num_channels)

    print(f"  Created test file: {filename}")
    return filepath


async def simulate_download(player, delay=2):
    """Simulate downloading audio files at intervals"""
    print("\n--- Simulating audio file downloads ---")

    for i in range(3):
        await asyncio.sleep(delay)
        filename = f"downloaded_audio_{i+1}.wav"
        print(f"\nSimulating download of {filename}...")
        create_test_audio_file(filename, duration=1, frequency=440 + (i * 100))
        print(f"  File downloaded to /audio directory")


async def main():
    print("=== Audio Download, Play, and Delete Test ===\n")

    # Initialize player
    print("Initializing AudioPlayer...")
    player = AudioPlayer()

    # Start the player loop task
    player_task = asyncio.create_task(player.run())
    await asyncio.sleep(0.5)

    # Start simulating downloads
    download_task = asyncio.create_task(simulate_download(player))

    # Wait for downloads and playback
    await download_task

    # Give extra time for final playback and deletion
    print("\nWaiting for final playback to complete...")
    await asyncio.sleep(5)

    # Check if all files were deleted
    remaining_files = player.api.get_audio_list()
    print(f"\nRemaining files in /audio: {remaining_files}")

    if not remaining_files:
        print("[SUCCESS] All files were successfully played and deleted!")
    else:
        print(f"[FAIL] {len(remaining_files)} file(s) still remain")

    print("\nStopping player...")
    player.stop()
    await player_task
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
