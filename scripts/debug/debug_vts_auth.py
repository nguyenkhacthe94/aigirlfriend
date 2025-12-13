"""
VTube Studio Diagnostic Tool with Authentication
Checks current model and available parameters using authentication
"""

import asyncio
import websockets
import json
import sys
import os

VTS_URL = "ws://localhost:8001"
TOKEN_FILE = "token.txt"

async def diagnose_vts():
    """Connect to VTS and print diagnostic information."""
    
    print("=" * 60)
    print("VTube Studio Diagnostic Tool (With Auth)")
    print("=" * 60)
    
    # Load authentication token
    token = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            token = f.read().strip()
        print(f"\n[OK] Loaded authentication token from {TOKEN_FILE}")
    else:
        print(f"\n[WARNING] No token file found. Run get_token.py first!")
        return
    
    try:
        print("\n[1/5] Connecting to VTube Studio...")
        async with websockets.connect(VTS_URL) as ws:
            print("[OK] Connected successfully!")
            
            # Authenticate
            print("\n[2/5] Authenticating...")
            auth_msg = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "auth-request",
                "messageType": "AuthenticationRequest",
                "data": {
                    "pluginName": "PythonClient",
                    "pluginDeveloper": "MyAIProject",
                    "authenticationToken": token
                }
            }
            await ws.send(json.dumps(auth_msg))
            auth_response = json.loads(await ws.recv())
            
            print(f"Auth Response: {json.dumps(auth_response, indent=2)}")
            
            if auth_response.get("data", {}).get("authenticated", False):
                print("[OK] Authentication successful!")
            else:
                print("[FAIL] Authentication failed!")
                print(f"Response: {json.dumps(auth_response, indent=2)}")
                return
            
            # Get API State
            print("\n[3/5] Checking API state...")
            msg = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "diagnostic-1",
                "messageType": "APIStateRequest"
            }
            await ws.send(json.dumps(msg))
            response = json.loads(await ws.recv())
            
            print(f"API State Response: {json.dumps(response, indent=2)}")
            
            if response.get("data", {}).get("active", False):
                print("[OK] VTube Studio API is active")
            else:
                print("[FAIL] VTube Studio API is NOT active")
                return
            
            # Get Current Model
            print("\n[4/5] Getting current model information...")
            msg["messageType"] = "CurrentModelRequest"
            msg["requestID"] = "diagnostic-2"
            await ws.send(json.dumps(msg))
            response = json.loads(await ws.recv())
            
            print(f"\nFull Model Response:")
            print(json.dumps(response, indent=2))
            
            model_data = response.get("data", {})
            
            print(f"\nParsed Model Information:")
            print(f"  Name: {model_data.get('modelName', 'Unknown')}")
            print(f"  ID: {model_data.get('modelID', 'Unknown')}")
            print(f"  Loaded: {model_data.get('modelLoaded', False)}")
            
            if not model_data.get('modelLoaded', False):
                print("\n[WARNING] No model is currently loaded in VTube Studio!")
                print("   Please load a model and try again.")
                return
            
            # Get Available Parameters
            print("\n[5/5] Fetching available parameters...")
            msg["messageType"] = "InputParameterListRequest"
            msg["requestID"] = "diagnostic-3"
            await ws.send(json.dumps(msg))
            response = json.loads(await ws.recv())
            
            parameters = response["data"]["defaultParameters"]
            custom_parameters = response["data"].get("customParameters", [])
            
            print(f"\n{'=' * 60}")
            print(f"AVAILABLE PARAMETERS ({len(parameters)} default + {len(custom_parameters)} custom)")
            print(f"{'=' * 60}\n")
            
            # Print default parameters
            print("DEFAULT PARAMETERS:")
            print(f"{'Parameter Name':<30} {'Min':<10} {'Max':<10} {'Default':<10}")
            print("-" * 60)
            
            for param in parameters:
                name = param['name']
                min_val = param['min']
                max_val = param['max']
                default_val = param['defaultValue']
                print(f"{name:<30} {min_val:<10.2f} {max_val:<10.2f} {default_val:<10.2f}")
            
            # Print custom parameters if any
            if custom_parameters:
                print("\nCUSTOM PARAMETERS:")
                print(f"{'Parameter Name':<30} {'Min':<10} {'Max':<10} {'Default':<10}")
                print("-" * 60)
                for param in custom_parameters:
                    name = param['name']
                    min_val = param['min']
                    max_val = param['max']
                    default_val = param['defaultValue']
                    print(f"{name:<30} {min_val:<10.2f} {max_val:<10.2f} {default_val:<10.2f}")
    
    except ConnectionRefusedError:
        print("\n[ERROR] Could not connect to VTube Studio")
        print("\nTroubleshooting:")
        print("  1. Make sure VTube Studio is running")
        print("  2. Go to Settings > Plugins")
        print("  3. Enable 'Start API' checkbox")
        print("  4. Verify port is 8001")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\nStarting VTube Studio diagnostics with authentication...\n")
    try:
        asyncio.run(diagnose_vts())
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted by user.")
        sys.exit(0)
    
    print("\n" + "=" * 60)
    print("Diagnostic complete!")
    print("=" * 60)
