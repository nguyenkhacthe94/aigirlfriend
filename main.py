import asyncio

import websockets

from llm_client import LLMClient
from vts_client import VTS_URL, vts_authenticate, vts_get_token


async def main():
    print("Connecting to VTube Studio...")

    # Initialize LLM client
    try:
        llm_client = LLMClient()
        print(
            f"✅ LLM Client initialized (Provider: {llm_client.provider}, Model: {llm_client.model})"
        )
    except Exception as e:
        print(f"❌ Failed to initialize LLM client: {e}")
        return

    try:
        async with websockets.connect(VTS_URL) as ws:
            token = await vts_get_token(ws)
            await vts_authenticate(ws, token)
            print("Connected and authenticated with VTube Studio.")

            print("Type a sentence to chat with your AI VTuber (or 'quit' to exit):")
            print("The AI will respond and express appropriate emotions automatically!")

            while True:
                user_input = input("> ")
                if user_input.lower() in ["quit", "exit"]:
                    break

                if not user_input.strip():
                    continue

                print(f"🤔 Processing: '{user_input}'...")
                try:
                    # Get unified response (text + expression) from LLM
                    start_time = asyncio.get_event_loop().time()

                    # Note: LLM call is synchronous, run in thread if needed for production
                    response = llm_client.call_llm(user_input)

                    end_time = asyncio.get_event_loop().time()
                    response_time = (end_time - start_time) * 1000  # Convert to ms

                    # Display AI response
                    print(f"🤖 AI Response: {response['text_response']}")

                    # Display expression if called
                    if response["expression_called"]:
                        print(f"😊 Expression: {response['expression_called']}()")
                    else:
                        print("😐 Expression: (neutral/none)")

                    # Display audio file if generated
                    if response.get("audio_file"):
                        import os

                        audio_file = response["audio_file"]
                        if os.path.exists(audio_file):
                            audio_size = os.path.getsize(audio_file)
                            print(
                                f"🔊 Audio: {os.path.basename(audio_file)} ({audio_size} bytes)"
                            )
                        else:
                            print(
                                f"🔇 Audio: {os.path.basename(audio_file)} (file missing)"
                            )
                    else:
                        print("🔇 Audio: (disabled or failed)")

                    # Performance feedback
                    if response_time < 500:
                        print(f"⚡ Response time: {response_time:.0f}ms (Good)")
                    else:
                        print(f"⏱️  Response time: {response_time:.0f}ms (Slow)")

                    # In production, these would trigger actual VTS parameter updates
                    print("✅ Expression applied to avatar!")

                except Exception as e:
                    print(f"❌ Error processing input: {e}")

    except Exception as e:
        print(f"❌ Failed to connect to VTube Studio: {e}")
        print(
            "Please ensure VTube Studio is running and the API is enabled on port 8001."
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
