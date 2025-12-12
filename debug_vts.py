"""
VTube Studio Diagnostic Tool
Checks current model and available parameters
"""

import asyncio
import websockets
import json
import sys

VTS_URL = "ws://localhost:8001"

async def diagnose_vts():
    """Connect to VTS and print diagnostic information."""
    
    print("=" * 60)
    print("VTube Studio Diagnostic Tool")
    print("=" * 60)
    
    try:
        print("\n[1/4] Connecting to VTube Studio...")
        async with websockets.connect(VTS_URL) as ws:
            print("✓ Connected successfully!")
            
            # Get API State
            print("\n[2/4] Checking API state...")
            msg = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "diagnostic-1",
                "messageType": "APIStateRequest"
            }
            await ws.send(json.dumps(msg))
            response = json.loads(await ws.recv())
            
            if response["data"]["active"]:
                print("✓ VTube Studio API is active")
            else:
                print("✗ VTube Studio API is NOT active")
                return
            
            # Get Current Model
            print("\n[3/4] Getting current model information...")
            msg["messageType"] = "CurrentModelRequest"
            msg["requestID"] = "diagnostic-2"
            await ws.send(json.dumps(msg))
            response = json.loads(await ws.recv())
            
            model_data = response["data"]
            
            print(f"\nCurrent Model:")
            print(f"  Name: {model_data.get('modelName', 'Unknown')}")
            print(f"  ID: {model_data.get('modelID', 'Unknown')}")
            print(f"  Loaded: {model_data.get('modelLoaded', False)}")
            
            if not model_data.get('modelLoaded', False):
                print("\n⚠ WARNING: No model is currently loaded in VTube Studio!")
                print("   Please load a model and try again.")
                return
            
            # Get Available Parameters
            print("\n[4/4] Fetching available parameters...")
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
            
            # Analysis and recommendations
            print("\n" + "=" * 60)
            print("ANALYSIS")
            print("=" * 60)
            
            # Check for chino11-specific parameters
            param_names = [p['name'] for p in parameters]
            
            chino11_params = [
                "PARAM_ANGLE_X", "PARAM_ANGLE_Y", "PARAM_ANGLE_Z",
                "PARAM_EYE_L_OPEN", "PARAM_EYE_R_OPEN",
                "PARAM_MOUTH_FORM", "PARAM_MOUTH_OPEN_Y",
                "PARAM_BROW_L_Y", "PARAM_BROW_R_Y"
            ]
            
            found_chino11 = sum(1 for p in chino11_params if p in param_names)
            
            print(f"\nChino11 Parameter Match: {found_chino11}/{len(chino11_params)} parameters found")
            
            if found_chino11 >= 7:
                print("✓ This appears to be the chino11 model (or compatible)")
                print("  Your expressions should work!")
            elif found_chino11 > 0:
                print("⚠ Partial match - some parameters exist but not all")
                print("  Some expressions may work, others may not")
            else:
                print("✗ This does NOT appear to be the chino11 model")
                print(f"  Current model: {model_data.get('modelName', 'Unknown')}")
                print("\nRECOMMENDATION:")
                print("  1. Load the chino11 model in VTube Studio")
                print("  2. Or create a new model config for the current model")
            
            # Missing parameters
            missing = [p for p in chino11_params if p not in param_names]
            if missing:
                print(f"\nMissing chino11 parameters:")
                for mp in missing:
                    print(f"  - {mp}")
    
    except ConnectionRefusedError:
        print("\n✗ ERROR: Could not connect to VTube Studio")
        print("\nTroubleshooting:")
        print("  1. Make sure VTube Studio is running")
        print("  2. Go to Settings > Plugins")
        print("  3. Enable 'Start API' checkbox")
        print("  4. Verify port is 8001")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\nStarting VTube Studio diagnostics...\n")
    try:
        asyncio.run(diagnose_vts())
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted by user.")
        sys.exit(0)
    
    print("\n" + "=" * 60)
    print("Diagnostic complete!")
    print("=" * 60)
