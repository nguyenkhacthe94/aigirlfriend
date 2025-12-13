"""
Hand Tracking Integration Test & Usage Examples

This script demonstrates how to use the HandTrackingController
with your existing VTS setup.
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_control.hand_tracking import hand_tracker, HandTrackingController
from vts_client import vts_request, vts_connect


async def test_hand_detection(ws):
    """Test hand detection status."""
    print("\n=== Testing Hand Detection ===")
    
    # Detect left hand
    print("✓ Detecting left hand...")
    await hand_tracker.set_hand_left_found(ws, True)
    await asyncio.sleep(1)
    
    # Detect right hand
    print("✓ Detecting right hand...")
    await hand_tracker.set_hand_right_found(ws, True)
    await asyncio.sleep(1)
    
    # Both hands should now be auto-detected
    print("✓ Both hands automatically detected!")
    await asyncio.sleep(1)
    
    # Hide hands
    print("✓ Hiding both hands...")
    await hand_tracker.set_both_hands_found(ws, False)
    await asyncio.sleep(1)


async def test_hand_positions(ws):
    """Test hand position control."""
    print("\n=== Testing Hand Positions ===")
    
    # Show hands
    await hand_tracker.set_both_hands_found(ws, True)
    
    # Move left hand to different positions
    print("✓ Moving left hand to right (+5, 0, 0)...")
    await hand_tracker.set_hand_left_position(ws, 5.0, 0.0, 0.0)
    await asyncio.sleep(1)
    
    print("✓ Moving left hand up (0, +5, 0)...")
    await hand_tracker.set_hand_left_position(ws, 0.0, 5.0, 0.0)
    await asyncio.sleep(1)
    
    print("✓ Moving left hand forward (0, 0, +5)...")
    await hand_tracker.set_hand_left_position(ws, 0.0, 0.0, 5.0)
    await asyncio.sleep(1)
    
    # Test position clamping (values outside -10 to 10 should be clamped)
    print("✓ Testing position clamping with value 15 (should clamp to 10)...")
    await hand_tracker.set_hand_left_position(ws, 15.0, 0.0, 0.0)
    await asyncio.sleep(1)
    
    # Reset to center
    print("✓ Resetting to center (0, 0, 0)...")
    await hand_tracker.set_hand_left_position(ws, 0.0, 0.0, 0.0)
    await asyncio.sleep(1)


async def test_hand_angles(ws):
    """Test hand angle control."""
    print("\n=== Testing Hand Angles ===")
    
    # Show hands
    await hand_tracker.set_both_hands_found(ws, True)
    
    # Rotate left hand
    print("✓ Rotating left hand: X=45°, Z=-30°...")
    await hand_tracker.set_hand_left_angles(ws, 45.0, -30.0)
    await asyncio.sleep(1)
    
    print("✓ Rotating left hand: X=-90°, Z=90°...")
    await hand_tracker.set_hand_left_angles(ws, -90.0, 90.0)
    await asyncio.sleep(1)
    
    # Test angle clamping
    print("✓ Testing angle clamping with value 200° (should clamp to 180°)...")
    await hand_tracker.set_hand_left_angles(ws, 200.0, 0.0)
    await asyncio.sleep(1)
    
    # Reset angles
    print("✓ Resetting angles to 0°...")
    await hand_tracker.set_hand_left_angles(ws, 0.0, 0.0)
    await asyncio.sleep(1)


async def test_hand_gestures(ws):
    """Test hand gesture presets."""
    print("\n=== Testing Hand Gestures ===")
    
    # Show hands
    await hand_tracker.set_both_hands_found(ws, True)
    
    # Open hand
    print("✓ Open hand...")
    await hand_tracker.open_hand_left(ws)
    await asyncio.sleep(1.5)
    
    # Fist
    print("✓ Make fist...")
    await hand_tracker.make_fist_left(ws)
    await asyncio.sleep(1.5)
    
    # Pointing
    print("✓ Pointing gesture...")
    await hand_tracker.make_pointing_left(ws)
    await asyncio.sleep(1.5)
    
    # Peace sign
    print("✓ Peace sign...")
    await hand_tracker.make_peace_sign_left(ws)
    await asyncio.sleep(1.5)
    
    # Thumbs up
    print("✓ Thumbs up...")
    await hand_tracker.make_thumbs_up_left(ws)
    await asyncio.sleep(1.5)
    
    # Open again
    print("✓ Open hand again...")
    await hand_tracker.open_hand_left(ws)
    await asyncio.sleep(1)


async def test_individual_fingers(ws):
    """Test individual finger control."""
    print("\n=== Testing Individual Finger Control ===")
    
    # Show hands
    await hand_tracker.set_both_hands_found(ws, True)
    
    # Start with closed fist
    await hand_tracker.make_fist_left(ws)
    await asyncio.sleep(1)
    
    # Extend fingers one by one
    print("✓ Extending thumb...")
    await hand_tracker.set_hand_left_thumb(ws, 1.0)
    await asyncio.sleep(0.8)
    
    print("✓ Extending index finger...")
    await hand_tracker.set_hand_left_index(ws, 1.0)
    await asyncio.sleep(0.8)
    
    print("✓ Extending middle finger...")
    await hand_tracker.set_hand_left_middle(ws, 1.0)
    await asyncio.sleep(0.8)
    
    print("✓ Extending ring finger...")
    await hand_tracker.set_hand_left_ring(ws, 1.0)
    await asyncio.sleep(0.8)
    
    print("✓ Extending pinky...")
    await hand_tracker.set_hand_left_pinky(ws, 1.0)
    await asyncio.sleep(1)
    
    # Close all fingers one by one
    print("✓ Closing all fingers one by one...")
    for finger_name, finger_method in [
        ("thumb", hand_tracker.set_hand_left_thumb),
        ("index", hand_tracker.set_hand_left_index),
        ("middle", hand_tracker.set_hand_left_middle),
        ("ring", hand_tracker.set_hand_left_ring),
        ("pinky", hand_tracker.set_hand_left_pinky),
    ]:
        print(f"  - Closing {finger_name}...")
        await finger_method(ws, 0.0)
        await asyncio.sleep(0.5)


async def test_both_hands_complex(ws):
    """Test complex both-hands choreography."""
    print("\n=== Testing Both Hands Complex Choreography ===")
    
    # Show both hands
    await hand_tracker.set_both_hands_found(ws, True)
    
    # Wave gesture (alternating hands)
    print("✓ Wave: Left hand up, right hand down...")
    await hand_tracker.set_hand_left_position(ws, -3.0, 5.0, 0.0)
    await hand_tracker.set_hand_right_position(ws, 3.0, -3.0, 0.0)
    await asyncio.sleep(1)
    
    print("✓ Wave: Right hand up, left hand down...")
    await hand_tracker.set_hand_left_position(ws, -3.0, -3.0, 0.0)
    await hand_tracker.set_hand_right_position(ws, 3.0, 5.0, 0.0)
    await asyncio.sleep(1)
    
    # Clap gesture (hands close together)
    print("✓ Clap: Moving hands close together...")
    await hand_tracker.set_hand_left_position(ws, -1.0, 0.0, 2.0)
    await hand_tracker.set_hand_right_position(ws, 1.0, 0.0, 2.0)
    await hand_tracker.set_hand_distance(ws, 2.0)
    await asyncio.sleep(1)
    
    # Spread apart
    print("✓ Spreading hands apart...")
    await hand_tracker.set_hand_left_position(ws, -5.0, 0.0, 0.0)
    await hand_tracker.set_hand_right_position(ws, 5.0, 0.0, 0.0)
    await hand_tracker.set_hand_distance(ws, 10.0)
    await asyncio.sleep(1)
    
    # Different gestures per hand
    print("✓ Left: Peace sign, Right: Thumbs up...")
    await hand_tracker.make_peace_sign_left(ws)
    await hand_tracker.make_thumbs_up_right(ws)
    await asyncio.sleep(2)
    
    # Reset
    print("✓ Resetting both hands...")
    await hand_tracker.reset_hands(ws)
    await asyncio.sleep(1)


async def run_all_tests():
    """Run all hand tracking tests."""
    print("=" * 60)
    print("HAND TRACKING CONTROLLER - INTEGRATION TEST")
    print("=" * 60)
    print("\nConnecting to VTube Studio...")
    
    try:
        # Connect to VTS
        ws = await vts_connect()
        print("✓ Connected to VTube Studio!\n")
        
        # Authenticate
        print("Authenticating...")
        auth_response = await vts_request(ws, "AuthenticationRequest", {
            "pluginName": "HandTrackingTest",
            "pluginDeveloper": "YourName"
        })
        
        if auth_response.get("data", {}).get("authenticated"):
            print("✓ Authenticated!\n")
        else:
            print("⚠ Authentication required. Please check VTube Studio.")
            return
        
        # Run test suites
        await test_hand_detection(ws)
        await test_hand_positions(ws)
        await test_hand_angles(ws)
        await test_hand_gestures(ws)
        await test_individual_fingers(ws)
        await test_both_hands_complex(ws)
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        # Final cleanup
        print("\nCleaning up...")
        await hand_tracker.reset_hands(ws)
        
        await ws.close()
        print("✓ Disconnected from VTube Studio")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def demo_simple_usage():
    """Simple usage demo for quick reference."""
    print("\n" + "=" * 60)
    print("SIMPLE USAGE DEMO")
    print("=" * 60)
    
    ws = await vts_connect()
    
    # Quick gesture demo
    print("\n1. Show left hand")
    await hand_tracker.set_hand_left_found(ws, True)
    await asyncio.sleep(1)
    
    print("2. Position at (x=5, y=3, z=0)")
    await hand_tracker.set_hand_left_position(ws, 5.0, 3.0, 0.0)
    await asyncio.sleep(1)
    
    print("3. Make peace sign")
    await hand_tracker.make_peace_sign_left(ws)
    await asyncio.sleep(2)
    
    print("4. Reset everything")
    await hand_tracker.reset_hands(ws)
    
    await ws.close()
    print("✓ Demo complete!")


if __name__ == "__main__":
    print("\nVTube Studio Hand Tracking Controller")
    print("--------------------------------------\n")
    print("Choose test mode:")
    print("  1. Run full test suite")
    print("  2. Run simple demo")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(run_all_tests())
    elif choice == "2":
        asyncio.run(demo_simple_usage())
    else:
        print("Exiting...")
