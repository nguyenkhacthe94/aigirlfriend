import pyaudio

py_audio = pyaudio.PyAudio()

print("=" * 60)
print("PyAudio Device List (Global Indices)")
print("=" * 60)
print("\nUse these indices for OUTPUT_DEVICE_INDEX in .env file\n")

# List all devices using GLOBAL device index
device_count = py_audio.get_device_count()

# Microphones
print("MICROPHONES (Input Devices):")
print("-" * 60)
for i in range(device_count):
    device_info = py_audio.get_device_info_by_index(i)
    # Check number of input channels
    if device_info.get('maxInputChannels') > 0:
        default_marker = " [DEFAULT]" if i == py_audio.get_default_input_device_info()['index'] else ""
        print(f"  {i:2d} - {device_info.get('name')}{default_marker}")

print("\n")

# Speakers
print("SPEAKERS (Output Devices):")
print("-" * 60)
for i in range(device_count):
    device_info = py_audio.get_device_info_by_index(i)
    # Check number of output channels
    if device_info.get('maxOutputChannels') > 0:
        default_marker = " [DEFAULT]" if i == py_audio.get_default_output_device_info()['index'] else ""
        print(f"  {i:2d} - {device_info.get('name')}{default_marker}")

print("\n" + "=" * 60)
print(f"Total devices found: {device_count}")
print("=" * 60)

py_audio.terminate()

