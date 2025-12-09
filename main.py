import asyncio
import websockets
from vts_client import vts_get_token, vts_authenticate, vts_inject_parameters, VTS_URL
from llm_client import get_emotion_for_text

# Mapping from emotion to VTube Studio parameters
EMOTION_MAP = {
    "neutral": {"FaceAngleX": 0.0, "MouthOpen": 0.0, "EyeOpenLeft": 1.0, "EyeOpenRight": 1.0},
    "happy": {"FaceAngleX": 5.0, "MouthOpen": 0.5, "EyeOpenLeft": 0.8, "EyeOpenRight": 0.8},
    "sad": {"FaceAngleX": -10.0, "MouthOpen": 0.0, "EyeOpenLeft": 0.6, "EyeOpenRight": 0.6},
    "angry": {"FaceAngleX": 0.0, "MouthOpen": 0.2, "EyeOpenLeft": 0.7, "EyeOpenRight": 0.7},
    "surprised": {"FaceAngleX": 0.0, "MouthOpen": 1.0, "EyeOpenLeft": 1.0, "EyeOpenRight": 1.0}
}

async def main():
    print("Connecting to VTube Studio...")
    try:
        async with websockets.connect(VTS_URL) as ws:
            token = await vts_get_token(ws)
            await vts_authenticate(ws, token)
            print("Connected and authenticated with VTube Studio.")

            print("Type a sentence to control the model (or 'quit' to exit):")
            while True:
                user_input = input("> ")
                if user_input.lower() in ["quit", "exit"]:
                    break
                
                if not user_input.strip():
                    continue

                print(f"Analyzing emotion for: '{user_input}'...")
                try:
                    # Get emotion from LLM
                    # Note: This is a synchronous call, might block the event loop briefly.
                    # In a production app, run this in a separate thread or make it async.
                    emotion_data = get_emotion_for_text(user_input)
                    emotion = emotion_data["emotion"]
                    intensity = emotion_data["intensity"]
                    print(f"Detected emotion: {emotion} (intensity: {intensity})")

                    # Get parameters for the emotion
                    params = EMOTION_MAP.get(emotion, EMOTION_MAP["neutral"]).copy()
                    
                    # Apply intensity to some parameters if needed (simple scaling example)
                    if "MouthOpen" in params:
                        params["MouthOpen"] *= intensity

                    # Inject into VTube Studio
                    await vts_inject_parameters(ws, params)
                    print("Model updated.")

                except Exception as e:
                    print(f"Error processing input: {e}")

    except Exception as e:
        print(f"Failed to connect to VTube Studio: {e}")
        print("Please ensure VTube Studio is running and the API is enabled on port 8001.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
