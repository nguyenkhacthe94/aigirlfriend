import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from audio_player.audioPlayer import AudioPlayer

async def main():
    print("=== Audio Playback Test ===\n")

    print("Initializing AudioPlayer...")
    player = AudioPlayer()

    audio_files = player.api.get_audio_list()
    print(f"Files found: {audio_files}\n")

    if not audio_files:
        print("No audio files found! Make sure you have .wav files in the audio/ directory")
        return

    # Start the player loop task
    player_task = asyncio.create_task(player.run())

    # Wait a moment for initialization
    await asyncio.sleep(0.5)

    # Play the first audio file
    print(f"Requesting to play: {audio_files[0]}")
    player.api.play_audio(audio_files[0])

    # Wait for playback to complete (give it plenty of time)
    print("Waiting for playback... (10 seconds)")
    await asyncio.sleep(10)

    print("\nStopping player...")
    player.stop()
    await player_task
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
