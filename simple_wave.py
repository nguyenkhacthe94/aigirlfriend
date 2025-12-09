import asyncio
import websockets
import time
from vts_client import vts_get_token, vts_authenticate, vts_inject_parameters, VTS_URL

async def simple_wave():
    print("Connecting to VTube Studio...")
    async with websockets.connect(VTS_URL) as ws:
        token = await vts_get_token(ws)
        await vts_authenticate(ws, token)
        print("Connected and authenticated.")

        # 1. Smile (Happy expression)
        print("Smiling...")
        smile_params = {
            "FaceAngleX": 0.0,
            "MouthOpen": 0.0,     # Closed mouth smile often looks better, or slight open
            "MouthForm": 1.0,     # Smile shape if supported
            "EyeOpenLeft": 0.8,
            "EyeOpenRight": 0.8,
            "CheekPuff": 0.0,
            "FaceAngry": 0.0,
            "FaceHappy": 1.0      # Some models use this
        }
        # Inject happy parameters
        await vts_inject_parameters(ws, smile_params)
        
        # 2. Wave (Simulated)
        # Since "Wave" isn't a standard parameter for all models, we'll try a few common ones
        # and also do a friendly head bob/sway.
        print("Waving...")
        
        # We'll oscillate some parameters to simulate movement
        start_time = time.time()
        while time.time() - start_time < 3.0: # Wave for 3 seconds
            t = time.time() * 5 # Speed of wave
            
            # Try to move arm if parameters exist (common standard names)
            # Values usually 0 to 1 or -1 to 1
            arm_val = (time.sin(t) + 1) / 2 
            
            wave_params = {
                "ParamArmL": arm_val, 
                "ParamHandL": arm_val,
                "FaceAngleZ": time.sin(t) * 5.0, # Head tilt sway
                "BodyAngleZ": time.sin(t) * 2.0  # Body sway
            }
            
            # Merge with smile params to keep smiling
            current_params = {**smile_params, **wave_params}
            
            await vts_inject_parameters(ws, current_params)
            await asyncio.sleep(0.05) # 20fps update

        # 3. Blink
        await blink(ws)
        await asyncio.sleep(0.5)
        await blink(ws)

        print("Done.")

async def blink(ws):
    """Make the model blink once."""
    print("Blinking...")
    # Close eyes
    await vts_inject_parameters(ws, {"EyeOpenLeft": 0.0, "EyeOpenRight": 0.0})
    await asyncio.sleep(0.15)
    # Open eyes
    await vts_inject_parameters(ws, {"EyeOpenLeft": 1.0, "EyeOpenRight": 1.0})

if __name__ == "__main__":
    # Need to import math for sin
    import math
    # Monkey patch time.sin for the loop above (oops, better just fix the code)
    time.sin = math.sin
    
    try:
        asyncio.run(simple_wave())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
