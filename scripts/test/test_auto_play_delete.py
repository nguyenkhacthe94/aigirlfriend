import asyncio
import sys
import os
import shutil

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from audio_player.audioPlayer import AudioPlayer

async def main():
    print("=== Auto-Play and Delete Test ===\n")

    # Initialize player
    print("Initializing AudioPlayer...")
    player = AudioPlayer()

    # Start the player loop task
    player_task = asyncio.create_task(player.run())
    await asyncio.sleep(1)

    # Copy test file to audio directory
    source_file = os.path.join(os.getcwd(), "audio", "file_example_WAV_1MG.wav")
    test_file = os.path.join(os.getcwd(), "audio", "test_audio.wav")

    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        print("Please ensure file_example_WAV_1MG.wav exists in the audio directory")
        player.stop()
        await player_task
        return

    print(f"\nCopying test file to audio directory...")
    shutil.copy(source_file, test_file)
    print(f"Created: {os.path.basename(test_file)}")

    print("\nWaiting for auto-play and deletion...")
    # Wait for the file to be detected, played, and deleted
    for i in range(30):  # Wait up to 30 seconds
        await asyncio.sleep(1)
        if not os.path.exists(test_file):
            print(f"\n✓ File was successfully played and deleted!")
            break
        if i % 5 == 0:
            print(f"  Waiting... ({i}s)")
    else:
        print(f"\n✗ File still exists after 30 seconds")
        if os.path.exists(test_file):
            os.remove(test_file)

    print("\nStopping player...")
    player.stop()
    await player_task
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
