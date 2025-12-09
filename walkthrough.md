# AI VTuber Controller - Walkthrough

I have implemented the AI VTuber Controller based on the `AI_VTuber.md` guide.

## Files Created

- **`vts_client.py`**: Handles the connection to VTube Studio.
- **`llm_client.py`**: Handles the connection to the local LLM.
- **`main.py`**: Combines both clients to control the model with text input.

## Prerequisites

1.  **Python 3.7+**: Ensure you have a modern Python version installed.
2.  **Dependencies**: Run `pip install websockets requests`.
3.  **VTube Studio**:
    *   Open VTube Studio.
    *   Go to Settings -> Plugins.
    *   Enable "Start API".
    *   Note the port (default is 8001).
4.  **Local LLM**:
    *   Ensure you have a local LLM running (e.g., Ollama).
    *   The default URL is `http://localhost:11434/api/generate`.
    *   The default model is `llama3`. You can change this in `llm_client.py` if needed.

## How to Run

1.  **Test VTube Studio Connection**:
    ```bash
    python3 main.py
    ```
    (Or run `python3 vts_client.py` for a standalone test)

2.  **First Run**:
    *   When you run the script for the first time, VTube Studio will show a popup asking to allow the plugin "Llama Live2D Controller".
    *   Click **Allow**.

3.  **Usage**:
    *   The `main.py` script will prompt you to type a sentence.
    *   Type something like "I am so happy today!" or "I am very angry!".
    *   The script will send the text to the LLM to detect the emotion.
    *   It will then send the corresponding parameters to VTube Studio to move the model.

## Troubleshooting

-   **Connection Refused (VTS)**: Make sure VTube Studio is running and the API is enabled.
-   **Connection Refused (LLM)**: Make sure your local LLM server is running.
-   **Authentication Failed**: If you denied the plugin request, you might need to delete `vts_token.txt` and try again.
