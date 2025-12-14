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
        self.currently_playing = None  # Track currently playing file for deletion
        self.queued_files = set()  # Track files that have been queued to avoid duplicates

        # API wrapper for compatibility if needed, or just methods on self
        self.api = self.API(self)

        print(f"AudioPlayer initialized (Python {sys.version})")
        print(f"OUTPUT_DEVICE_INDEX set to: {OUTPUT_DEVICE_INDEX}")

        if not self.enabled:
            return

        # Set up audio directory
        self.audio_dir = os.path.join(os.getcwd(), "audio")

        if not os.path.exists(self.audio_dir):
            print(f"Creating audio directory at {self.audio_dir}")
            os.makedirs(self.audio_dir)
        else:
            print(f"Audio directory: {self.audio_dir}")

    def _scan_for_new_audio_files(self):
        """
        Scan the audio directory for new .wav files that haven't been queued yet.
        Returns the list of newly found files.
        """
        if not os.path.exists(self.audio_dir):
            return []

        new_files = []
        for file in os.listdir(self.audio_dir):
            if file.lower().endswith(".wav"):
                file_path = os.path.join(self.audio_dir, file)
                # Only add if not already queued and not currently playing
                if file_path not in self.queued_files and file_path != self.currently_playing:
                    new_files.append(file_path)

        return new_files

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
            # Small delay to ensure all file handles are released (Windows)
            time.sleep(0.05)

    async def run(self):
        print("AudioPlayer service started.")
        print("Monitoring audio directory for new .wav files...")

        last_scan_time = 0
        scan_interval = 1.0  # Scan every 1 second

        while not self.terminate:
            if not self.enabled:
                await asyncio.sleep(1)
                continue

            current_time = asyncio.get_event_loop().time()

            # Scan for new audio files periodically
            if current_time - last_scan_time >= scan_interval:
                new_files = self._scan_for_new_audio_files()
                for file_path in new_files:
                    self.play_queue.put(file_path)
                    self.queued_files.add(file_path)  # Track as queued
                    print(f"Detected new audio file: {os.path.basename(file_path)}")
                last_scan_time = current_time

            # If we are not currently playing audio, unset the abort flag
            if not self.is_speaking:
                self.abort_flag = False

            # Check if there are any audio files to play
            if self.play_queue.qsize() > 0:
                file_path = self.play_queue.get()

                # Check if file still exists (might have been deleted)
                if not os.path.exists(file_path):
                    print(f"Audio file no longer exists: {file_path}")
                    self.queued_files.discard(file_path)  # Remove from queued set
                    continue

                print(f"Playing: {os.path.basename(file_path)}")
                self.is_speaking = True
                self.currently_playing = file_path

                try:
                    # Run the entire playback in a background thread to avoid blocking
                    await asyncio.to_thread(self._play_audio_blocking, file_path)

                    # After successful playback, delete the file
                    # Add small delay and retry logic for Windows file lock issues
                    deleted = False
                    for attempt in range(3):
                        try:
                            await asyncio.sleep(0.1)  # Small delay to ensure file handles are released
                            os.remove(file_path)
                            print(f"Deleted: {os.path.basename(file_path)}")
                            deleted = True
                            break
                        except PermissionError as e:
                            if attempt < 2:
                                print(f"Deletion attempt {attempt + 1} failed, retrying...")
                                await asyncio.sleep(0.5)  # Wait longer before retry
                            else:
                                print(f"Error deleting file after 3 attempts: {e}")
                        except Exception as e:
                            print(f"Error deleting file {file_path}: {e}")
                            break

                    self.queued_files.discard(file_path)  # Remove from queued set

                except Exception as e:
                    print(f"Error playing audio file: {e}")
                    import traceback
                    traceback.print_exc()
                    # Remove from queued set on error
                    self.queued_files.discard(file_path)

                self.is_speaking = False
                self.currently_playing = None

            await asyncio.sleep(0.1)

    def stop(self):
        self.terminate = True

    class API:
        def __init__(self, outer):
            self.outer = outer

        def get_audio_list(self):
            """Get list of current .wav files in the audio directory"""
            if not os.path.exists(self.outer.audio_dir):
                return []

            filenames = []
            for file in os.listdir(self.outer.audio_dir):
                if file.lower().endswith(".wav"):
                    filenames.append(file)
            return filenames

        def play_audio(self, file_path):
            """Manually queue an audio file for playback"""
            # If file_path is just a filename, construct full path
            if not os.path.isabs(file_path):
                file_path = os.path.join(self.outer.audio_dir, file_path)

            if os.path.exists(file_path):
                self.outer.play_queue.put(file_path)
            else:
                print(f"Audio file not found: {file_path}")

        def pause_audio(self):
            self.outer.paused = True

        def resume_audio(self):
            self.outer.paused = False

        def stop_playing(self):
            self.outer.abort_flag = True
