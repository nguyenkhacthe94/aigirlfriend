import asyncio
import websockets
import time
import math
from vts_client import vts_get_token, vts_authenticate, vts_inject_parameters, VTS_URL

# --- Expression Functions ---

async def smile(ws):
    """Make the model smile."""
    print("Expression: Smile")
    params = {
        "FaceAngleX": 0.0,
        "MouthOpen": 0.0,
        "MouthForm": 1.0,
        "EyeOpenLeft": 0.8,
        "EyeOpenRight": 0.8,
        "CheekPuff": 0.0,
        "FaceAngry": 0.0,
        "FaceHappy": 1.0
    }
    await vts_inject_parameters(ws, params)

async def laugh(ws):
    """Make the model laugh."""
    print("Expression: Laugh")
    # Laughing usually involves open mouth, happy eyes, maybe some movement
    params = {
        "MouthOpen": 1.0,
        "MouthForm": 1.0,
        "EyeOpenLeft": 0.0, # Happy squint
        "EyeOpenRight": 0.0,
        "FaceHappy": 1.0,
        "BodyAngleZ": 5.0   # Slight lean
    }
    await vts_inject_parameters(ws, params)
    
    # Optional: Add a little bounce for laughter
    for _ in range(3):
        await vts_inject_parameters(ws, {"BodyAngleY": 2.0})
        await asyncio.sleep(0.1)
        await vts_inject_parameters(ws, {"BodyAngleY": -2.0})
        await asyncio.sleep(0.1)
    await vts_inject_parameters(ws, {"BodyAngleY": 0.0})

async def angry(ws):
    """Make the model look angry."""
    print("Expression: Angry")
    params = {
        "FaceAngry": 1.0,
        "FaceHappy": 0.0,
        "MouthForm": -1.0, # Frown
        "EyeOpenLeft": 0.8,
        "EyeOpenRight": 0.8,
        "Brows": -1.0      # Furrowed brows (if supported, often mapped to FaceAngry)
    }
    await vts_inject_parameters(ws, params)

async def blink(ws):
    """Make the model blink once."""
    print("Expression: Blink")
    # Close eyes
    await vts_inject_parameters(ws, {"EyeOpenLeft": 0.0, "EyeOpenRight": 0.0})
    await asyncio.sleep(0.15)
    # Open eyes
    await vts_inject_parameters(ws, {"EyeOpenLeft": 1.0, "EyeOpenRight": 1.0})

# --- Main Control Loop ---

async def interactive_control():
    print("Connecting to VTube Studio...")
    try:
        async with websockets.connect(VTS_URL) as ws:
            token = await vts_get_token(ws)
            await vts_authenticate(ws, token)
            print("Connected and authenticated.")
            print("Commands: blink, smile, laugh, angry, quit")

            # We need to run the input loop in a way that doesn't block the event loop entirely if we wanted background tasks,
            # but for this simple request, we can just use a blocking input in a separate thread or just block since we react to commands.
            # However, `input()` is blocking. To keep it simple and safe within async, we'll use run_in_executor.
            
            loop = asyncio.get_running_loop()

            while True:
                # Run input() in a separate thread so it doesn't block the async loop (good practice)
                cmd = await loop.run_in_executor(None, input, "Enter command: ")
                cmd = cmd.strip().lower()

                if cmd == "quit":
                    print("Exiting...")
                    break
                elif cmd == "blink":
                    await blink(ws)
                elif cmd == "smile":
                    await smile(ws)
                elif cmd == "laugh":
                    await laugh(ws)
                elif cmd == "angry":
                    await angry(ws)
                else:
                    print(f"Unknown command: {cmd}")

    except ConnectionRefusedError:
        print("Could not connect to VTube Studio. Is it running and the API enabled?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(interactive_control())
    except KeyboardInterrupt:
        print("\nExiting...")

