"""
VTube Studio Authentication Token Generator
This script connects to VTube Studio and requests an authentication token.
"""

import json
import websocket
import time

# VTube Studio WebSocket configuration
VTUBE_STUDIO_WS = "ws://localhost:8001"
PLUGIN_NAME = "PythonClient"
PLUGIN_DEVELOPER = "MyAIProject"
TOKEN_FILE = "token.txt"


def request_auth_token():
    """Connect to VTube Studio and request an authentication token."""
    
    print("=" * 60)
    print("VTube Studio Authentication Token Generator")
    print("=" * 60)
    print(f"\nConnecting to VTube Studio at {VTUBE_STUDIO_WS}...")
    
    try:
        # Create WebSocket connection
        ws = websocket.create_connection(VTUBE_STUDIO_WS)
        print("✓ Connected successfully!")
        
        # Prepare authentication token request
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "AuthTokenRequest",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": PLUGIN_NAME,
                "pluginDeveloper": PLUGIN_DEVELOPER
            }
        }
        
        # Send the request
        print(f"\nSending authentication request...")
        print(f"  Plugin Name: {PLUGIN_NAME}")
        print(f"  Plugin Developer: {PLUGIN_DEVELOPER}")
        ws.send(json.dumps(auth_request))
        
        # Prompt user to allow the plugin
        print("\n" + "!" * 60)
        print("⚠  ACTION REQUIRED ⚠")
        print("!" * 60)
        print("\nPlease check your VTube Studio window NOW!")
        print("You should see a popup asking you to ALLOW this plugin.")
        print("Click the 'Allow' button to continue...")
        print("\nWaiting for your response...")
        
        # Wait for response
        response = ws.recv()
        response_data = json.loads(response)
        
        # Check if we received the token
        if response_data.get("messageType") == "AuthenticationTokenResponse":
            if "authenticationToken" in response_data.get("data", {}):
                token = response_data["data"]["authenticationToken"]
                
                # Save token to file
                with open(TOKEN_FILE, "w") as f:
                    f.write(token)
                
                print("\n" + "=" * 60)
                print("✓ SUCCESS!")
                print("=" * 60)
                print(f"\nAuthentication token received and saved to: {TOKEN_FILE}")
                print(f"Token: {token[:20]}...{token[-20:]}")
                print("\nYou can now use this token in your VTube Studio scripts!")
                print("=" * 60)
                
            else:
                print("\n✗ Error: No authentication token in response")
                print(f"Response: {json.dumps(response_data, indent=2)}")
        else:
            print(f"\n✗ Unexpected response type: {response_data.get('messageType')}")
            print(f"Response: {json.dumps(response_data, indent=2)}")
        
        # Close connection
        ws.close()
        
    except websocket.WebSocketException as e:
        print(f"\n✗ WebSocket Error: {e}")
        print("\nMake sure VTube Studio is running and the API is enabled!")
        print("(Settings → Allow plugins → Enable API)")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    request_auth_token()
