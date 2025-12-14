"""
Multi-Model VTuber Controller with LLM Emotion Detection

This is an updated version of main.py that supports multiple Live2D models
using the models/ package architecture.

Usage:
    python main_multi_model.py --model chino11
"""

import asyncio
import argparse
import websockets
from vts_client import vts_get_token, vts_authenticate, vts_inject_parameters, VTS_URL
from llm_client import LLMClient
from models import get_model, list_models


async def main(model_name: str = "chino11"):
    """
    Main controller loop with dynamic model loading.
    
    Args:
        model_name: Name of the Live2D model to control
    """
    # Initialize LLM client for unified responses
    try:
        llm_client = LLMClient()
        print(f"LLM Client initialized: {llm_client.provider} - {llm_client.model}")
    except Exception as e:
        print(f"Error initializing LLM client: {e}")
        return
    
    # Load the specified model configuration
    try:
        model = get_model(model_name)
        print(f"Loaded model: {model}")
        print(f"Available emotions: {', '.join(model.available_emotions)}")
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Available models: {', '.join(list_models())}")
        return
    
    print(f"\nConnecting to VTube Studio...")
    try:
        async with websockets.connect(VTS_URL) as ws:
            token = await vts_get_token(ws)
            await vts_authenticate(ws, token)
            print(f"Connected and authenticated with VTube Studio.")
            print(f"Controlling model: {model_name}")
            
            print("\nType a sentence to control the model (or 'quit' to exit):")
            while True:
                user_input = input("> ")
                if user_input.lower() in ["quit", "exit"]:
                    break
                
                if not user_input.strip():
                    continue

                print(f"Getting response for: '{user_input}'...")
                try:
                    # Get unified response from LLM
                    response = llm_client.call_llm(user_input)
                    text_response = response.get("text_response", "")
                    expression_called = response.get("expression_called")
                    
                    print(f"AI Response: {text_response}")
                    if expression_called:
                        print(f"Expression called: {expression_called}")
                    
                    # For backward compatibility with emotion-based model system,
                    # map expression functions to basic emotions
                    expression_to_emotion = {
                        "smile": ("happy", 0.6),
                        "laugh": ("happy", 1.0),
                        "angry": ("angry", 0.8),
                        "sad": ("sad", 0.7),
                        "wow": ("surprised", 0.8),
                        "shy": ("neutral", 0.3),  # shy doesn't map well to basic emotions
                        "love": ("happy", 0.9),
                        "agree": ("neutral", 0.4),
                        "disagree": ("angry", 0.3),
                        "yap": ("neutral", 0.5),
                        "blink": ("neutral", 0.1),
                    }
                    
                    # Use expression if available, otherwise default to neutral
                    if expression_called and expression_called in expression_to_emotion:
                        emotion, intensity = expression_to_emotion[expression_called]
                        print(f"Mapped to emotion: {emotion} (intensity: {intensity:.2f})")
                    else:
                        emotion = "neutral"
                        intensity = 0.5
                        print(f"Using default: {emotion} (intensity: {intensity:.2f})")

                    # Get parameters from model with intensity scaling
                    if emotion in model.emotions:
                        params = model.apply_intensity(emotion, intensity)
                    else:
                        print(f"Warning: Emotion '{emotion}' not found, using neutral")
                        params = model.emotions["neutral"]

                    # Inject into VTube Studio
                    await vts_inject_parameters(ws, params)
                    print("Model updated.")

                except Exception as e:
                    print(f"Error processing input: {e}")

    except Exception as e:
        print(f"Failed to connect to VTube Studio: {e}")
        print("Please ensure VTube Studio is running and the API is enabled on port 8001.")


if __name__ == "__main__":
    # Add command-line argument support
    parser = argparse.ArgumentParser(
        description="Multi-Model VTuber Controller with Expression Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive emotion control
  python main_multi_model.py --model chino11
  
  # Test a specific emotion
  python main_multi_model.py --model chino11 --emotion happy --intensity 0.8
  
  # Test a micro-expression
  python main_multi_model.py --model chino11 --micro raise_eyebrows
  
  # Test a composite expression
  python main_multi_model.py --model chino11 --composite sarcastic
  
  # List available actions
  python main_multi_model.py --model chino11 --list
        """
    )
    parser.add_argument(
        "--model",
        type=str,
        default="chino11",
        help=f"Model to control (available: {', '.join(list_models())})"
    )
    parser.add_argument(
        "--emotion",
        type=str,
        help="Test a specific emotion preset (e.g., happy, sad, angry)"
    )
    parser.add_argument(
        "--intensity",
        type=float,
        default=1.0,
        help="Emotion intensity (0.0-1.0, default: 1.0)"
    )
    parser.add_argument(
        "--micro",
        type=str,
        help="Test a micro-expression (e.g., raise_eyebrows, blink, smirk)"
    )
    parser.add_argument(
        "--composite",
        type=str,
        help="Test a composite expression (e.g., sarcastic, listening, empathetic)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available emotions, micro-expressions, and composite expressions"
    )
    
    args = parser.parse_args()
    
    # Load model
    try:
        model = get_model(args.model)
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Available models: {', '.join(list_models())}")
        exit(1)
    
    # Handle list command
    if args.list:
        print(f"\n=== {model.model_name} Available Actions ===\n")
        
        print(f"Emotions ({len(model.available_emotions)}):")
        for emotion in model.available_emotions:
            print(f"  - {emotion}")
        
        print(f"\nMicro-Expressions ({len(model.available_micro_expressions)}):")
        for micro in model.available_micro_expressions:
            print(f"  - {micro}")
        
        print(f"\nComposite Expressions ({len(model.available_composite_expressions)}):")
        for comp in model.available_composite_expressions:
            print(f"  - {comp}")
        
        print("\nUsage:")
        print(f"  python main_multi_model.py --model {args.model} --emotion <name>")
        print(f"  python main_multi_model.py --model {args.model} --micro <name>")
        print(f"  python main_multi_model.py --model {args.model} --composite <name>")
        exit(0)
    
    # Handle one-shot testing
    if args.emotion or args.micro or args.composite:
        async def test_expression():
            print(f"Connecting to VTube Studio...")
            try:
                async with websockets.connect(VTS_URL) as ws:
                    token = await vts_get_token(ws)
                    await vts_authenticate(ws, token)
                    print(f"Connected!")
                    
                    if args.emotion:
                        if args.emotion not in model.available_emotions:
                            print(f"Error: Unknown emotion '{args.emotion}'")
                            print(f"Available: {', '.join(model.available_emotions)}")
                            return
                        
                        print(f"Testing emotion: {args.emotion} (intensity: {args.intensity})")
                        params = model.apply_intensity(args.emotion, args.intensity)
                        await vts_inject_parameters(ws, params)
                        print("✓ Emotion applied successfully!")
                    
                    elif args.micro:
                        if args.micro not in model.available_micro_expressions:
                            print(f"Error: Unknown micro-expression '{args.micro}'")
                            print(f"Available: {', '.join(model.available_micro_expressions)}")
                            return
                        
                        print(f"Testing micro-expression: {args.micro}")
                        params = model.get_micro(args.micro)
                        await vts_inject_parameters(ws, params)
                        print("✓ Micro-expression applied successfully!")
                        
                        # Auto-revert blinks
                        if "blink" in args.micro or "wink" in args.micro:
                            await asyncio.sleep(0.15)
                            await vts_inject_parameters(ws, {
                                "PARAM_EYE_L_OPEN": 1.0,
                                "PARAM_EYE_R_OPEN": 1.0
                            })
                            print("✓ Eyes reopened")
                    
                    elif args.composite:
                        if args.composite not in model.available_composite_expressions:
                            print(f"Error: Unknown composite expression '{args.composite}'")
                            print(f"Available: {', '.join(model.available_composite_expressions)}")
                            return
                        
                        print(f"Testing composite expression: {args.composite}")
                        params = model.get_composite(args.composite)
                        await vts_inject_parameters(ws, params)
                        print("✓ Composite expression applied successfully!")
                    
            except Exception as e:
                print(f"Failed to connect to VTube Studio: {e}")
                print("Please ensure VTube Studio is running and the API is enabled on port 8001.")
        
        try:
            asyncio.run(test_expression())
        except KeyboardInterrupt:
            print("\nExiting...")
    else:
        # Interactive mode
        try:
            asyncio.run(main(args.model))
        except KeyboardInterrupt:
            print("\nExiting...")

