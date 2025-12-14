#!/usr/bin/env python3
"""
Debug script for testing audio file cleanup and management functionality.
This script is for development use only.

Usage:
    python scripts/debug/debug_audio_cleanup.py
"""
import os
import sys
import time
from datetime import datetime, timedelta

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from llm_client import LLMClient


def create_test_files():
    """Create test audio files with different timestamps."""
    print("=== Creating Test Files ===")

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_dir = os.path.join(project_root, "audio")

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir, exist_ok=True)
        print(f"Created audio directory: {audio_dir}")

    # Create files with different ages
    now = datetime.now()
    test_files = [
        ("response_recent.wav", now - timedelta(hours=1)),  # 1 hour ago
        ("response_yesterday.wav", now - timedelta(days=1)),  # 1 day ago
        ("response_week_old.wav", now - timedelta(days=7)),  # 7 days ago
        ("response_month_old.wav", now - timedelta(days=30)),  # 30 days ago
    ]

    created_files = []
    for filename, file_time in test_files:
        file_path = os.path.join(audio_dir, filename)

        # Create a small dummy WAV file
        with open(file_path, "wb") as f:
            f.write(
                b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00"
            )  # Minimal WAV header

        # Set file modification time
        timestamp = file_time.timestamp()
        os.utime(file_path, (timestamp, timestamp))

        created_files.append((file_path, file_time))
        print(
            f"Created: {filename} (modified: {file_time.strftime('%Y-%m-%d %H:%M:%S')})"
        )

    return created_files


def test_cleanup_functionality():
    """Test the cleanup functionality with different settings."""
    print("\n=== Testing Cleanup Functionality ===")

    # Test with different cleanup settings
    cleanup_settings = [0, 3, 7, 14, 30]  # days

    for days in cleanup_settings:
        print(f"\nTesting cleanup with {days} days threshold:")

        # Set environment variable for this test
        old_cleanup_days = os.environ.get("TTS_CLEANUP_DAYS")
        os.environ["TTS_CLEANUP_DAYS"] = str(days)

        try:
            # Create new client with updated settings
            client = LLMClient()

            # Run cleanup
            cleanup_count = client.cleanup_old_audio_files()
            print(f"  Cleaned up: {cleanup_count} files")

            # List remaining files
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            audio_dir = os.path.join(project_root, "audio")
            if os.path.exists(audio_dir):
                remaining_files = [
                    f for f in os.listdir(audio_dir) if f.endswith(".wav")
                ]
                print(f"  Remaining files: {len(remaining_files)}")
                for f in remaining_files:
                    file_path = os.path.join(audio_dir, f)
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    print(f"    {f} (modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")

        except Exception as e:
            print(f"  Error: {e}")

        finally:
            # Restore original setting
            if old_cleanup_days is not None:
                os.environ["TTS_CLEANUP_DAYS"] = old_cleanup_days
            elif "TTS_CLEANUP_DAYS" in os.environ:
                del os.environ["TTS_CLEANUP_DAYS"]


def test_directory_management():
    """Test audio directory creation and management."""
    print("\n=== Testing Directory Management ===")

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_dir = os.path.join(project_root, "audio")

    # Test directory creation
    print(f"Audio directory path: {audio_dir}")
    print(f"Directory exists: {os.path.exists(audio_dir)}")

    if os.path.exists(audio_dir):
        # Check permissions
        print(f"Directory readable: {os.access(audio_dir, os.R_OK)}")
        print(f"Directory writable: {os.access(audio_dir, os.W_OK)}")

        # List all files
        all_files = os.listdir(audio_dir)
        audio_files = [f for f in all_files if f.endswith(".wav")]
        other_files = [f for f in all_files if not f.endswith(".wav")]

        print(f"Total files: {len(all_files)}")
        print(f"Audio files (.wav): {len(audio_files)}")
        print(f"Other files: {len(other_files)}")

        if other_files:
            print("Non-audio files found:")
            for f in other_files:
                print(f"  {f}")


def test_file_size_management():
    """Test behavior with different file sizes."""
    print("\n=== Testing File Size Management ===")

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_dir = os.path.join(project_root, "audio")

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir, exist_ok=True)

    # Calculate total size of audio files
    total_size = 0
    file_count = 0

    if os.path.exists(audio_dir):
        for filename in os.listdir(audio_dir):
            if filename.endswith(".wav"):
                file_path = os.path.join(audio_dir, filename)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    total_size += size
                    file_count += 1

    print(f"Audio files: {file_count}")
    print(f"Total size: {total_size} bytes ({total_size / 1024:.1f} KB)")

    if total_size > 0:
        avg_size = total_size / file_count
        print(f"Average file size: {avg_size:.1f} bytes")

    # Check for unusually large or small files
    if os.path.exists(audio_dir):
        for filename in os.listdir(audio_dir):
            if filename.endswith(".wav"):
                file_path = os.path.join(audio_dir, filename)
                size = os.path.getsize(file_path)
                if size == 0:
                    print(f"WARNING: Empty file found: {filename}")
                elif size < 100:  # Very small for audio file
                    print(f"WARNING: Unusually small file: {filename} ({size} bytes)")


def cleanup_test_files():
    """Remove test files created by this script."""
    print("\n=== Cleaning Up Test Files ===")

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    audio_dir = os.path.join(project_root, "audio")

    if not os.path.exists(audio_dir):
        print("No audio directory found")
        return

    test_file_patterns = [
        "response_recent.wav",
        "response_yesterday.wav",
        "response_week_old.wav",
        "response_month_old.wav",
    ]

    cleaned_count = 0
    for filename in test_file_patterns:
        file_path = os.path.join(audio_dir, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed: {filename}")
                cleaned_count += 1
            except Exception as e:
                print(f"Could not remove {filename}: {e}")

    print(f"Cleaned up {cleaned_count} test files")


def main():
    """Run all audio cleanup debug tests."""
    print("Audio Cleanup Debug Script")
    print("=" * 40)

    try:
        # Create test files for cleanup testing
        test_files = create_test_files()

        # Test cleanup functionality
        test_cleanup_functionality()

        # Test directory management
        test_directory_management()

        # Test file size management
        test_file_size_management()

    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # Always try to clean up test files
        try:
            cleanup_test_files()
        except Exception as e:
            print(f"Cleanup failed: {e}")

    print("\n" + "=" * 40)
    print("Cleanup debug tests completed")


if __name__ == "__main__":
    main()
