"""
Test script to control VTube Studio model (chino11)
Demonstrates how to move head, eyes, and mouth
"""

import asyncio
import websockets
import json
import os
import time

VTS_URL = "ws://localhost:8001"
TOKEN_FILE = "token.txt"

async def control_model():
    """Connect and control the VTube Studio model."""
    
    # Load token
    if not os.path.exists(TOKEN_FILE):
        print("[ERROR] token.txt not found. Run get_token.py first!")
        return
    
    with open(TOKEN_FILE, 'r') as f:
        token = f.read().strip()
    
    print("=" * 60)
    print("VTube Studio Model Control Test")
    print("=" * 60)
    
    async with websockets.connect(VTS_URL) as ws:
        # Authenticate
        print("\n[1/3] Authenticating...")
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
        response = json.loads(await ws.recv())
        
        if not response.get("data", {}).get("authenticated", False):
            print("[ERROR] Authentication failed!")
            return
        
        print("[OK] Authenticated!")
        
        # Test 1: Move head left and right
        print("\n[2/3] Testing head movement...")
        print("  Moving head LEFT...")
        await set_parameter(ws, "FaceAngleY", -20.0)
        await asyncio.sleep(1)
        
        print("  Moving head RIGHT...")
        await set_parameter(ws, "FaceAngleY", 20.0)
        await asyncio.sleep(1)
        
        print("  Center head...")
        await set_parameter(ws, "FaceAngleY", 0.0)
        await asyncio.sleep(0.5)
        
        # Test 2: Control eyes
        print("\n[3/3] Testing eye control...")
        print("  Closing eyes...")
        await set_parameter(ws, "EyeOpenLeft", 0.0)
        await set_parameter(ws, "EyeOpenRight", 0.0)
        await asyncio.sleep(1)
        
        print("  Opening eyes...")
        await set_parameter(ws, "EyeOpenLeft", 1.0)
        await set_parameter(ws, "EyeOpenRight", 1.0)
        await asyncio.sleep(0.5)
        
        # Test 3: Smile
        print("\n  Making smile...")
        await set_parameter(ws, "MouthSmile", 1.0)
        await asyncio.sleep(1)
        
        print("  Neutral expression...")
        await set_parameter(ws, "MouthSmile", 0.0)
        await asyncio.sleep(0.5)
        
        # Test 4: Open mouth
        print("\n  Opening mouth...")
        await set_parameter(ws, "MouthOpen", 0.8)
        await asyncio.sleep(1)
        
        print("  Closing mouth...")
        await set_parameter(ws, "MouthOpen", 0.0)
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Model control test completed!")
        print("=" * 60)
        print("\nYour chino11 model is fully controllable!")
        print("\nKey parameters you can use:")
        print("  - FaceAngleX, FaceAngleY, FaceAngleZ (head rotation)")
        print("  - EyeOpenLeft, EyeOpenRight (eyes)")
        print("  - MouthOpen, MouthSmile (mouth)")
        print("  - BrowLeftY, BrowRightY (eyebrows)")


async def set_parameter(ws, parameter_name, value):
    """Set a parameter value in VTube Studio."""
    msg = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": f"set_{parameter_name}",
        "messageType": "InjectParameterDataRequest",
        "data": {
            "parameterValues": [
                {
                    "id": parameter_name,
                    "value": value
                }
            ]
        }
    }
    await ws.send(json.dumps(msg))
    response = json.loads(await ws.recv())
    return response


if __name__ == "__main__":
    print("\nStarting model control test...")
    print("Watch your VTube Studio window!\n")
    
    try:
        asyncio.run(control_model())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
