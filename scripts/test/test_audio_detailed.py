import wave
import pyaudio
import os

# Test direct PyAudio playback without asyncio
def test_direct_playback():
    audio_file = os.path.join(os.getcwd(), "audio", "file_example_WAV_1MG.wav")

    if not os.path.exists(audio_file):
        print(f"Audio file not found: {audio_file}")
        return

    print(f"Testing direct playback of: {audio_file}\n")

    # Open WAV file
    wf = wave.open(audio_file, 'rb')

    # Get audio parameters
    channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    framerate = wf.getframerate()

    print(f"Audio info:")
    print(f"  Channels: {channels}")
    print(f"  Sample width: {sample_width} bytes")
    print(f"  Frame rate: {framerate} Hz")
    print(f"  Duration: {wf.getnframes() / framerate:.2f} seconds")

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # List device info
    device_index = 6
    device_info = p.get_device_info_by_index(device_index)
    print(f"\nDevice {device_index} info:")
    print(f"  Name: {device_info['name']}")
    print(f"  Max output channels: {device_info['maxOutputChannels']}")
    print(f"  Default sample rate: {device_info['defaultSampleRate']}")

    # Open stream
    print(f"\nOpening stream on device {device_index}...")
    try:
        stream = p.open(
            format=p.get_format_from_width(sample_width),
            channels=channels,
            rate=framerate,
            output_device_index=device_index,
            output=True
        )

        print("Stream opened successfully!")
        print("Playing audio...")

        # Read and play audio in chunks
        chunk_size = 1024
        data = wf.readframes(chunk_size)
        chunks_written = 0

        while len(data) > 0:
            stream.write(data)
            chunks_written += 1
            data = wf.readframes(chunk_size)

        print(f"Finished playing {chunks_written} chunks")

        # Clean up
        stream.stop_stream()
        stream.close()

    except Exception as e:
        print(f"Error during playback: {e}")
        import traceback
        traceback.print_exc()
    finally:
        p.terminate()
        wf.close()

    print("\nDone!")

if __name__ == "__main__":
    test_direct_playback()
