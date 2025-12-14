import os
import asyncio
import queue
import pyaudio
import wave
import sys
from dotenv import load_dotenv

load_dotenv()

# Default to system default output device if not specified
# Can be overridden with OUTPUT_DEVICE_INDEX environment variable
OUTPUT_DEVICE_INDEX = int(os.getenv('OUTPUT_DEVICE_INDEX')) if os.getenv('OUTPUT_DEVICE_INDEX') else None

class AudioPlayer:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.play_queue = queue.SimpleQueue()
        self.abort_flag = False
        self.paused = False
        self.is_speaking = False  # Replaces signals.AI_speaking
        self.terminate = False    # Control flag for the run loop

        # API wrapper for compatibility if needed, or just methods on self
        self.api = self.API(self)

        print(f"AudioPlayer initialized (Python {sys.version})")
        print(f"OUTPUT_DEVICE_INDEX set to: {OUTPUT_DEVICE_INDEX}")

        if not self.enabled:
            return

        # Find all audio files in the audio directory
        self.audio_files = []
        self.audio_dir = os.path.join(os.getcwd(), "audio")
        
        if os.path.exists(self.audio_dir):
            for dirpath, dirnames, filenames in os.walk(self.audio_dir):
                for file in filenames:
                    # Only support WAV for now to avoid pydub/audioop issues on Python 3.13
                    if file.lower().endswith(".wav"):
                        audio = self.Audio(file, os.path.join(dirpath, file))
                        self.audio_files.append(audio)
                        print(f"Found audio: {file}")
        else:
            print(f"Warning: Audio directory not found at {self.audio_dir}")

    def _play_audio_blocking(self, audio_path):
        """
        Blocking audio playback method that runs in a background thread.
        This keeps the event loop free while audio plays.
        """
        import time

        wf = None
        p = None
        stream = None

        try:
            # Open WAV file
            wf = wave.open(audio_path, 'rb')
            p = pyaudio.PyAudio()

            print(f"Opening audio stream with device index: {OUTPUT_DEVICE_INDEX}")
            print(f"Audio format: {wf.getnchannels()} channels, {wf.getframerate()} Hz, {wf.getsampwidth()} bytes per sample")

            # Open stream
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output_device_index=OUTPUT_DEVICE_INDEX,
                output=True,
                frames_per_buffer=1024
            )

            print(f"Audio stream opened successfully")

            # Read and write audio data
            chunk_size = 1024
            data = wf.readframes(chunk_size)

            while len(data) > 0:
                # Check pause flag
                while self.paused:
                    if self.abort_flag:
                        break
                    time.sleep(0.1)

                # Check abort flag
                if self.abort_flag:
                    self.abort_flag = False
                    print("Audio playback aborted")
                    break

                # Write audio chunk (blocking)
                stream.write(data)

                # Read next chunk
                data = wf.readframes(chunk_size)

            print("Audio playback completed")

        except Exception as e:
            print(f"Error during audio playback: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Clean up resources
            if stream:
                stream.stop_stream()
                stream.close()
            if p:
                p.terminate()
            if wf:
                wf.close()

    async def run(self):
        print("AudioPlayer service started.")
        while not self.terminate:
            if not self.enabled:
                await asyncio.sleep(1)
                continue

            # If we are not currently playing audio, unset the abort flag
            self.abort_flag = False

            # Check if there are any audio files to play
            if self.play_queue.qsize() > 0:
                file_name = self.play_queue.get()
                print(f"Request to play: {file_name}")
                
                # Special command to play all
                if file_name == "__ALL__":
                    print("Queueing all songs...")
                    for audio in self.audio_files:
                         self.play_queue.put(audio.file_name)
                    continue

                found = False
                for audio in self.audio_files:
                    if audio.file_name == file_name:
                        found = True
                        print(f"Playing {audio.path}")
                        self.is_speaking = True

                        try:
                            # Run the entire playback in a background thread to avoid blocking
                            await asyncio.to_thread(self._play_audio_blocking, audio.path)
                        except Exception as e:
                            print(f"Error playing audio file: {e}")
                            import traceback
                            traceback.print_exc()

                        self.is_speaking = False
                        break
                
                if not found:
                    print(f"Audio file not found: {file_name}")

            await asyncio.sleep(0.1)

    def stop(self):
        self.terminate = True

    class Audio:
        def __init__(self, file_name, path):
            self.file_name = file_name
            self.path = path

    class API:
        def __init__(self, outer):
            self.outer = outer

        def get_audio_list(self):
            filenames = []
            for audio in self.outer.audio_files:
                filenames.append(audio.file_name)
            return filenames

        def play_audio(self, file_name):
            self.stop_playing() # Stop current before playing new
            self.outer.play_queue.put(file_name)
            
        def play_all(self):
            self.outer.play_queue.put("__ALL__")

        def pause_audio(self):
            self.outer.paused = True

        def resume_audio(self):
            self.outer.paused = False

        def stop_playing(self):
            self.outer.abort_flag = True
