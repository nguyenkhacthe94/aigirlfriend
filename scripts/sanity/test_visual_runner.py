"""
Hiyori Model Parameter Visual Tester

This standalone script tests all 74 parameters from hiyori_parameters.json
by cycling each parameter through Min -> Max -> Default values in VTube Studio.

Usage: python scripts/sanity/test_visual_runner.py
"""

import asyncio
import json
import os
import websockets
from pathlib import Path
import time


# =============================================================================
# VTS Connection Configuration
# =============================================================================

VTS_URL = "ws://localhost:8001"
PLUGIN_NAME = "Llama Live2D Controller"  # Using existing plugin name to reuse token
PLUGIN_DEV = "YourName"
TOKEN_FILE = "vts_token.txt"

# Test timing (in seconds)
WAIT_TIME = 0.2


# =============================================================================
# VTS API Functions (Self-contained)
# =============================================================================

async def vts_send(ws, message: dict) -> dict:
    """Send a JSON message to VTS and return the JSON response."""
    await ws.send(json.dumps(message))
    resp_raw = await ws.recv()
    return json.loads(resp_raw)


async def vts_request_token(ws) -> str:
    """Request an authentication token from VTS and save it."""
    msg = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "token-request-1",
        "messageType": "AuthenticationTokenRequest",
        "data": {
            "pluginName": PLUGIN_NAME,
            "pluginDeveloper": PLUGIN_DEV
        }
    }
    resp = await vts_send(ws, msg)
    token = resp["data"]["authenticationToken"]
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token)
    return token


async def vts_get_token(ws) -> str:
    """Return existing token if present, otherwise request a new one."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return await vts_request_token(ws)


async def vts_authenticate(ws, token: str) -> None:
    """Authenticate plugin with VTS API using a stored token."""
    msg = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "auth-1",
        "messageType": "AuthenticationRequest",
        "data": {
            "pluginName": PLUGIN_NAME,
            "pluginDeveloper": PLUGIN_DEV,
            "authenticationToken": token
        }
    }
    resp = await vts_send(ws, msg)
    if not resp["data"].get("authenticated", False):
        raise RuntimeError("VTS authentication failed")


async def vts_inject_parameters(ws, params: dict) -> None:
    """
    Inject Live2D parameter values.
    
    Args:
        ws: WebSocket connection
        params: dict like {"ParamAngleX": 0.5, "ParamMouthOpen": 0.8}
    """
    msg = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "inject-params",
        "messageType": "InjectParameterDataRequest",
        "data": {
            "faceFound": True,
            "mode": "set",
            "parameterValues": [
                {"id": pid, "value": val} for pid, val in params.items()
            ]
        }
    }
    await vts_send(ws, msg)


# =============================================================================
# Parameter Testing Logic
# =============================================================================

def load_parameters(json_path: str) -> list:
    """Load parameters from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


async def test_parameter(ws, param: dict, index: int, total: int) -> bool:
    """
    Test a single parameter by cycling through min, max, default values.
    
    Args:
        ws: WebSocket connection
        param: Parameter dict with id, min, max, default
        index: Current parameter index (1-based)
        total: Total number of parameters
        
    Returns:
        True if test succeeded, False otherwise
    """
    param_id = param['id']
    param_name = param.get('name', param_id)
    min_val = param['min']
    max_val = param['max']
    default_val = param['default']
    
    print(f"\n[{index}/{total}] Testing {param_id}", end='', flush=True)
    
    try:
        # Set to minimum
        print(f" → Min({min_val})", end='', flush=True)
        await vts_inject_parameters(ws, {param_id: min_val})
        await asyncio.sleep(WAIT_TIME)
        
        # Set to maximum
        print(f" → Max({max_val})", end='', flush=True)
        await vts_inject_parameters(ws, {param_id: max_val})
        await asyncio.sleep(WAIT_TIME)
        
        # Reset to default
        print(f" → Default({default_val})", end='', flush=True)
        await vts_inject_parameters(ws, {param_id: default_val})
        await asyncio.sleep(WAIT_TIME)
        
        print(f" ✓ OK", flush=True)
        return True
        
    except Exception as e:
        print(f" ✗ FAILED: {e}", flush=True)
        return False


async def run_visual_test():
    """Main test runner."""
    print("=" * 80)
    print("HIYORI MODEL PARAMETER VISUAL TESTER")
    print("=" * 80)
    print()
    
    # Load parameters
    params_file = Path("model_control/hiyori_parameters.json")
    
    if not params_file.exists():
        print(f"❌ Error: {params_file} not found!")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Expected path: {params_file.absolute()}")
        return
    
    print(f"📁 Loading parameters from: {params_file}")
    parameters = load_parameters(str(params_file))
    total_params = len(parameters)
    print(f"✓ Loaded {total_params} parameters\n")
    
    # Connect to VTS
    print(f"🔌 Connecting to VTube Studio at {VTS_URL}...")
    
    try:
        async with websockets.connect(VTS_URL) as ws:
            print("✓ Connected!\n")
            
            # Authenticate
            print("🔐 Authenticating...")
            token = await vts_get_token(ws)
            await vts_authenticate(ws, token)
            print("✓ Authenticated!\n")
            
            print("=" * 80)
            print("STARTING PARAMETER TESTS")
            print("=" * 80)
            print(f"Each parameter will cycle: Min → Max → Default (0.2s delay each)")
            print()
            
            # Track results
            start_time = time.time()
            success_count = 0
            failed_params = []
            
            # Test each parameter
            for i, param in enumerate(parameters, 1):
                success = await test_parameter(ws, param, i, total_params)
                if success:
                    success_count += 1
                else:
                    failed_params.append(param['id'])
            
            # Summary
            elapsed_time = time.time() - start_time
            
            print()
            print("=" * 80)
            print("TEST SUMMARY")
            print("=" * 80)
            print(f"Total Parameters: {total_params}")
            print(f"✓ Passed: {success_count}")
            print(f"✗ Failed: {len(failed_params)}")
            print(f"⏱ Time Elapsed: {elapsed_time:.2f}s")
            
            if failed_params:
                print(f"\n❌ Failed Parameters:")
                for param_id in failed_params:
                    print(f"   - {param_id}")
            else:
                print(f"\n🎉 ALL PARAMETERS TESTED SUCCESSFULLY!")
            
            print("=" * 80)
            
    except websockets.exceptions.WebSocketException as e:
        print(f"\n❌ WebSocket Connection Error: {e}")
        print(f"   Make sure VTube Studio is running and the API is enabled.")
        print(f"   (Settings → Allow plugins to control VTube Studio)")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                  HIYORI MODEL PARAMETER VISUAL TESTER                      ║")
    print("║                                                                            ║")
    print("║  This script will test all 74 parameters from hiyori_parameters.json      ║")
    print("║  by cycling each one through: Min → Max → Default                         ║")
    print("║                                                                            ║")
    print("║  Watch your VTube Studio window to verify visual changes!                 ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    asyncio.run(run_visual_test())
