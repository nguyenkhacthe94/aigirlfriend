import asyncio
import json
import os
import websockets

VTS_URL = "ws://localhost:8001"
PLUGIN_NAME = "Llama Live2D Controller"
PLUGIN_DEV = "YourName"
TOKEN_FILE = "vts_token.txt"

async def vts_send(ws, message: dict) -> dict:
    """Send a JSON message to VTS and return the JSON response."""
    if hasattr(ws, "lock"):
        async with ws.lock:
            await ws.send(json.dumps(message))
            resp_raw = await ws.recv()
    else:
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

async def vts_inject_parameters(ws, params: dict, face_found: bool = True) -> None:
    """
    Inject Live2D parameter values.

    params: dict like {"FaceAngleX": 10.0, "MouthOpen": 0.8}
    """
    msg = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "inject-1",
        "messageType": "InjectParameterDataRequest",
        "data": {
            "faceFound": face_found,
            "mode": "set",
            "parameterValues": [
                {"id": pid, "value": val} for pid, val in params.items()
            ]
        }
    }
    await vts_send(ws, msg)

async def vts_request_input_parameter_list(ws) -> dict:
    """Request the list of available input parameters."""
    msg = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "param-list-1",
        "messageType": "InputParameterListRequest"
    }
    resp = await vts_send(ws, msg)
    return resp["data"]

async def vts_test_movement():
    """Connect to VTS, authenticate, and send a simple test movement."""
    async with websockets.connect(VTS_URL) as ws:
        token = await vts_get_token(ws)
        await vts_authenticate(ws, token)

        test_params = {
            "FaceAngleX": 15.0,  # tilt head
            "MouthOpen": 0.8     # open mouth
        }
        await vts_inject_parameters(ws, test_params)
        print("Test movement sent to VTS.")

if __name__ == "__main__":
    asyncio.run(vts_test_movement())
