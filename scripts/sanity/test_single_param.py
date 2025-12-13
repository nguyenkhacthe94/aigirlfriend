"""
Test a single VTube Studio parameter with a specific value
Usage: python test_single_param.py <parameter_name> <value> [duration]
Example: python test_single_param.py FaceAngleY 20.0 2
"""

import asyncio
import websockets
import json
import os
import sys

VTS_URL = "ws://localhost:8001"
TOKEN_FILE = "token.txt"


async def test_single_parameter(param_name: str, value: float, duration: float = 2.0):
    """Test a single parameter by setting it to a value, then resetting."""
    
    # Load token
    if not os.path.exists(TOKEN_FILE):
        print("[ERROR] token.txt not found. Run get_token.py first!")
        return
    
    with open(TOKEN_FILE, 'r') as f:
        token = f.read().strip()
    
    print("=" * 70)
    print(f"Testing Parameter: {param_name}")
    print(f"Value: {value}")
    print(f"Duration: {duration} seconds")
    print("=" * 70)
    
    async with websockets.connect(VTS_URL) as ws:
        # Authenticate
        auth_msg = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "auth",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": "PythonClient",
                "pluginDeveloper": "MyAIProject",
                "authenticationToken": token
            }
        }
        await ws.send(json.dumps(auth_msg))
        await ws.recv()
        
        print(f"\n[OK] Setting {param_name} = {value}...")
        
        # Set the parameter
        msg = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "set_param",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "parameterValues": [
                    {"id": param_name, "value": value}
                ]
            }
        }
        await ws.send(json.dumps(msg))
        response = json.loads(await ws.recv())
        
        if response.get("messageType") == "APIError":
            print(f"[ERROR] {response.get('data', {}).get('message', 'Unknown error')}")
            return
        
        print(f"[OK] Applied! Watch your model for {duration} seconds...")
        await asyncio.sleep(duration)
        
        # Reset to 0 (or middle value for ranges that include 0)
        print(f"\n[OK] Resetting {param_name} to 0...")
        msg["data"]["parameterValues"][0]["value"] = 0.0
        await ws.send(json.dumps(msg))
        await ws.recv()
        
        print(f"\n{'=' * 70}")
        print("[SUCCESS] Test complete!")
        print("=" * 70)


def print_usage():
    """Print usage instructions."""
    print("\n" + "=" * 70)
    print("Test Single VTube Studio Parameter")
    print("=" * 70)
    print("\nUsage:")
    print("  python test_single_param.py <parameter_name> <value> [duration]")
    print("\nArguments:")
    print("  parameter_name  - Name of the parameter (e.g., FaceAngleY)")
    print("  value          - Value to set (e.g., 20.0)")
    print("  duration       - How long to hold the value in seconds (default: 2.0)")
    print("\nExamples:")
    print("  python test_single_param.py FaceAngleY 20.0")
    print("  python test_single_param.py EyeOpenLeft 0.5 3")
    print("  python test_single_param.py MouthSmile 1.0 1.5")
    print("  python test_single_param.py TongueOut 1.0")
    print("\nCommon Parameters:")
    print("  Head:      FaceAngleX, FaceAngleY, FaceAngleZ")
    print("  Eyes:      EyeOpenLeft, EyeOpenRight")
    print("  Mouth:     MouthOpen, MouthSmile")
    print("  Eyebrows:  BrowLeftY, BrowRightY")
    print("  Express:   FaceAngry, TongueOut, CheekPuff")
    print("\nTip: Run 'python show_all_parameters.py' to see all 88 parameters")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    param_name = sys.argv[1]
    
    try:
        value = float(sys.argv[2])
    except ValueError:
        print(f"[ERROR] Invalid value: {sys.argv[2]}")
        print("Value must be a number (e.g., 20.0, 0.5, 1.0)")
        sys.exit(1)
    
    duration = 2.0
    if len(sys.argv) > 3:
        try:
            duration = float(sys.argv[3])
        except ValueError:
            print(f"[ERROR] Invalid duration: {sys.argv[3]}")
            print("Duration must be a number in seconds (e.g., 2.0, 1.5)")
            sys.exit(1)
    
    try:
        asyncio.run(test_single_parameter(param_name, value, duration))
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
