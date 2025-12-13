"""
Complete VTube Studio Parameter Reference for chino11
Shows all 88 available parameters organized by category
"""

import asyncio
import websockets
import json
import os

VTS_URL = "ws://localhost:8001"
TOKEN_FILE = "token.txt"

# All 88 available parameters organized by category
PARAMETERS = {
    "HEAD_MOVEMENT": {
        "FacePositionX": (-15.0, 15.0, "Head position left/right"),
        "FacePositionY": (-15.0, 15.0, "Head position up/down"),
        "FacePositionZ": (-10.0, 10.0, "Head position forward/back"),
        "FaceAngleX": (-30.0, 30.0, "Head tilt up/down"),
        "FaceAngleY": (-30.0, 30.0, "Head turn left/right"),
        "FaceAngleZ": (-90.0, 90.0, "Head lean left/right"),
    },
    
    "EYES": {
        "EyeOpenLeft": (0.0, 1.0, "Left eye openness (0=closed, 1=open)"),
        "EyeOpenRight": (0.0, 1.0, "Right eye openness"),
        "EyeLeftX": (-1.0, 1.0, "Left eye look left/right"),
        "EyeLeftY": (-1.0, 1.0, "Left eye look up/down"),
        "EyeRightX": (-1.0, 1.0, "Right eye look left/right"),
        "EyeRightY": (-1.0, 1.0, "Right eye look up/down"),
    },
    
    "MOUTH": {
        "MouthOpen": (0.0, 1.0, "Mouth openness"),
        "MouthSmile": (0.0, 1.0, "Smile intensity"),
        "MouthX": (-1.0, 1.0, "Mouth position left/right"),
    },
    
    "EYEBROWS": {
        "Brows": (0.0, 1.0, "Both eyebrows raised"),
        "BrowLeftY": (0.0, 1.0, "Left eyebrow position"),
        "BrowRightY": (0.0, 1.0, "Right eyebrow position"),
    },
    
    "EXPRESSIONS": {
        "FaceAngry": (0.0, 1.0, "Angry expression"),
        "TongueOut": (0.0, 1.0, "Tongue visibility"),
        "CheekPuff": (0.0, 1.0, "Puffy cheeks"),
    },
    
    "MOUSE_TRACKING": {
        "MousePositionX": (-1.0, 1.0, "Mouse position X on screen"),
        "MousePositionY": (-1.0, 1.0, "Mouse position Y on screen"),
    },
    
    "VOICE_LIP_SYNC": {
        "VoiceVolume": (0.0, 1.0, "Voice volume level"),
        "VoiceFrequency": (0.0, 1.0, "Voice frequency/pitch"),
        "VoiceVolumePlusMouthOpen": (0.0, 1.0, "Combined volume + mouth"),
        "VoiceFrequencyPlusMouthSmile": (0.0, 1.0, "Combined frequency + smile"),
        "VoiceA": (0.0, 1.0, "Vowel A detection"),
        "VoiceI": (0.0, 1.0, "Vowel I detection"),
        "VoiceU": (0.0, 1.0, "Vowel U detection"),
        "VoiceE": (0.0, 1.0, "Vowel E detection"),
        "VoiceO": (0.0, 1.0, "Vowel O detection"),
        "VoiceSilence": (0.0, 1.0, "Silence detection"),
    },
    
    "HAND_TRACKING": {
        "HandLeftFound": (0.0, 1.0, "Left hand detected"),
        "HandRightFound": (0.0, 1.0, "Right hand detected"),
        "BothHandsFound": (0.0, 1.0, "Both hands detected"),
        "HandDistance": (0.0, 10.0, "Distance between hands"),
        "HandLeftPositionX": (0.0, 10.0, "Left hand X position"),
        "HandLeftPositionY": (-10.0, 10.0, "Left hand Y position"),
        "HandLeftPositionZ": (-10.0, 10.0, "Left hand Z position"),
        "HandRightPositionX": (0.0, 10.0, "Right hand X position"),
        "HandRightPositionY": (-10.0, 10.0, "Right hand Y position"),
        "HandRightPositionZ": (-10.0, 10.0, "Right hand Z position"),
        "HandLeftAngleX": (-180.0, 180.0, "Left hand rotation X"),
        "HandLeftAngleZ": (-180.0, 180.0, "Left hand rotation Z"),
        "HandRightAngleX": (-180.0, 180.0, "Right hand rotation X"),
        "HandRightAngleZ": (-180.0, 180.0, "Right hand rotation Z"),
        "HandLeftOpen": (0.0, 1.0, "Left hand openness"),
        "HandRightOpen": (0.0, 1.0, "Right hand openness"),
    },
    
    "FINGER_TRACKING_LEFT": {
        "HandLeftFinger_1_Thumb": (0.0, 1.0, "Left thumb"),
        "HandLeftFinger_2_Index": (0.0, 1.0, "Left index finger"),
        "HandLeftFinger_3_Middle": (0.0, 1.0, "Left middle finger"),
        "HandLeftFinger_4_Ring": (0.0, 1.0, "Left ring finger"),
        "HandLeftFinger_5_Pinky": (0.0, 1.0, "Left pinky"),
    },
    
    "FINGER_TRACKING_RIGHT": {
        "HandRightFinger_1_Thumb": (0.0, 1.0, "Right thumb"),
        "HandRightFinger_2_Index": (0.0, 1.0, "Right index finger"),
        "HandRightFinger_3_Middle": (0.0, 1.0, "Right middle finger"),
        "HandRightFinger_4_Ring": (0.0, 1.0, "Right ring finger"),
        "HandRightFinger_5_Pinky": (0.0, 1.0, "Right pinky"),
    },
    
    "MOCOPI_BODY_TRACKING": {
        "MocopiConnected": (0.0, 1.0, "Mocopi device connected"),
        "MocopiHipAngleZ": (-30.0, 30.0, "Hip rotation Z"),
        "MocopiAngleX": (-30.0, 30.0, "Body angle X"),
        "MocopiAngleY": (-30.0, 30.0, "Body angle Y"),
        "MocopiAngleZ": (-30.0, 30.0, "Body angle Z"),
        "MocopiBodyAngleX": (-10.0, 10.0, "Body rotation X"),
        "MocopiBodyAngleY": (-10.0, 10.0, "Body rotation Y"),
        "MocopiBodyAngleZ": (-10.0, 10.0, "Body rotation Z"),
        "MocopiBodyPositionX": (-1.0, 1.0, "Body position X"),
        "MocopiBodyPositionY": (-1.0, 1.0, "Body position Y"),
        "MocopiBodyPositionZ": (-1.0, 1.0, "Body position Z"),
    },
    
    "MOCOPI_ARMS": {
        "MocopiUpperArmLeftAngleY": (-90.0, 90.0, "Left upper arm Y"),
        "MocopiUpperArmLeftAngleZ": (-180.0, 180.0, "Left upper arm Z"),
        "MocopiUpperArmRightAngleY": (-90.0, 90.0, "Right upper arm Y"),
        "MocopiUpperArmRightAngleZ": (-180.0, 180.0, "Right upper arm Z"),
        "MocopiLowerArmLeftAngleX": (-180.0, 180.0, "Left lower arm X"),
        "MocopiLowerArmLeftAngleY": (-90.0, 90.0, "Left lower arm Y"),
        "MocopiLowerArmLeftAngleZ": (-180.0, 180.0, "Left lower arm Z"),
        "MocopiLowerArmRightAngleX": (-180.0, 180.0, "Right lower arm X"),
        "MocopiLowerArmRightAngleY": (-90.0, 90.0, "Right lower arm Y"),
        "MocopiLowerArmRightAngleZ": (-180.0, 180.0, "Right lower arm Z"),
    },
    
    "MOCOPI_LEGS": {
        "MocopiUpperLegLeftAngleY": (-30.0, 30.0, "Left upper leg Y"),
        "MocopiUpperLegLeftAngleZ": (-30.0, 30.0, "Left upper leg Z"),
        "MocopiUpperLegRightAngleY": (-30.0, 30.0, "Right upper leg Y"),
        "MocopiUpperLegRightAngleZ": (-30.0, 30.0, "Right upper leg Z"),
        "MocopiLowerLegLeftAngleY": (-30.0, 30.0, "Left lower leg Y"),
        "MocopiLowerLegLeftAngleZ": (-30.0, 30.0, "Left lower leg Z"),
        "MocopiLowerLegRightAngleY": (-30.0, 30.0, "Right lower leg Y"),
        "MocopiLowerLegRightAngleZ": (-30.0, 30.0, "Right lower leg Z"),
    },
}


def print_all_parameters():
    """Print all available parameters organized by category."""
    print("=" * 80)
    print("COMPLETE VTUBE STUDIO PARAMETER REFERENCE FOR CHINO11")
    print("=" * 80)
    print(f"\nTotal: 88 Parameters across {len(PARAMETERS)} categories\n")
    
    total = 0
    for category, params in PARAMETERS.items():
        print(f"\n{'-' * 80}")
        print(f"[{category.replace('_', ' ')}] ({len(params)} parameters)")
        print(f"{'-' * 80}")
        
        for param_name, (min_val, max_val, description) in params.items():
            print(f"  {param_name:<35} [{min_val:>7} to {max_val:>7}]  {description}")
            total += 1
    
    print(f"\n{'=' * 80}")
    print(f"Total parameters: {total}")
    print("=" * 80)


async def demo_category(category_name):
    """Demonstrate controlling parameters in a specific category."""
    if category_name not in PARAMETERS:
        print(f"Category '{category_name}' not found!")
        return
    
    # Load token
    if not os.path.exists(TOKEN_FILE):
        print("[ERROR] token.txt not found. Run get_token.py first!")
        return
    
    with open(TOKEN_FILE, 'r') as f:
        token = f.read().strip()
    
    params = PARAMETERS[category_name]
    
    print(f"\n{'=' * 80}")
    print(f"TESTING: {category_name.replace('_', ' ')}")
    print(f"{'=' * 80}\n")
    
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
        
        print("Watch your VTube Studio model!\n")
        
        # Test each parameter in the category
        for param_name, (min_val, max_val, description) in params.items():
            print(f"Testing: {param_name} - {description}")
            
            # Set to max
            await set_parameter(ws, param_name, max_val)
            await asyncio.sleep(0.8)
            
            # Reset to default (usually middle or 0)
            default_val = 0.0 if min_val <= 0 <= max_val else min_val
            await set_parameter(ws, param_name, default_val)
            await asyncio.sleep(0.3)
        
        print(f"\n[OK] {category_name} test complete!")


async def set_parameter(ws, parameter_name, value):
    """Set a parameter value."""
    msg = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": f"set_{parameter_name}",
        "messageType": "InjectParameterDataRequest",
        "data": {
            "parameterValues": [
                {"id": parameter_name, "value": value}
            ]
        }
    }
    await ws.send(json.dumps(msg))
    await ws.recv()


if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 80)
    print("VTube Studio - Complete Parameter Reference")
    print("=" * 80)
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Demo mode - test a specific category
        if len(sys.argv) > 2:
            category = sys.argv[2].upper()
            asyncio.run(demo_category(category))
        else:
            print("\nUsage: python show_all_parameters.py demo <CATEGORY>")
            print("\nAvailable categories:")
            for cat in PARAMETERS.keys():
                print(f"  - {cat}")
    else:
        # List all parameters
        print_all_parameters()
        print("\n[TIP] To test a category, run:")
        print("   python show_all_parameters.py demo HEAD_MOVEMENT")
        print("   python show_all_parameters.py demo EYES")
        print("   python show_all_parameters.py demo MOUTH")
        print("   etc.\n")
