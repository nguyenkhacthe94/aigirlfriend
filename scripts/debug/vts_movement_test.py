
import asyncio
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from model_control.vts_expressions import (
    smile, laugh, angry, blink, wow, agree, disagree, yap, shy, sad, love, hello
)

COMMANDS = {
    "smile": smile,
    "laugh": laugh,
    "angry": angry,
    "blink": blink,
    "wow": wow,
    "agree": agree,
    "disagree": disagree,
    "yap": yap,
    "shy": shy,
    "sad": sad,
    "love": love,
    "hello": hello
}

async def main():
    print("VTS Expression Tester")
    print(f"Available commands: {', '.join(COMMANDS.keys())}")
    print("Type 'quit' or 'exit' to stop.\n")

    loop = asyncio.get_running_loop()

    while True:
        try:
            cmd_input = await loop.run_in_executor(None, input, "> ")
            cmd = cmd_input.strip().lower()

            if cmd in ["quit", "exit"]:
                print("Exiting...")
                break
            
            if not cmd:
                continue

            if cmd in COMMANDS:
                await COMMANDS[cmd]()
            else:
                print(f"Unknown command: {cmd}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error executing command: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
