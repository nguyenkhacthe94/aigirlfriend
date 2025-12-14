
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from audio_player.audioPlayer import AudioPlayer

async def main():
    print("Initializing AudioPlayer...")
    player = AudioPlayer()
    
    print("Files found:", player.api.get_audio_list())
    
    # Start the player loop task
    player_task = asyncio.create_task(player.run())
    
    # Let it run for a bit
    await asyncio.sleep(2)
    
    print("Stopping player...")
    player.stop()
    await player_task
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
