````markdown
# AI VTuber Controller – Coding Agent Guideline

This document tells you (the coding agent) how to write Python code that:

1. Connects to **VTube Studio** via WebSocket and can move a Live2D model.
2. Connects to a **local LLaMA LLM** and uses its output.

Use this as a blueprint for creating actual Python modules.

---

## 1. Connect to VTube Studio

### 1.1. Environment & Imports

**Goal:** Create a Python module (e.g. `vts_client.py`) that can:

- Connect to the VTS WebSocket API
- Authenticate a plugin
- Inject parameter values to control the model

**Steps:**

1. Ensure Python has these packages:

   - `websockets`
   - `asyncio`
   - `json`
   - `os`

2. At the top of `vts_client.py`, import:

   ```python
   import asyncio
   import json
   import os
   import websockets
````

3. Define basic constants:

   ```python
   VTS_URL = "ws://localhost:8001"
   PLUGIN_NAME = "Llama Live2D Controller"
   PLUGIN_DEV = "YourName"
   TOKEN_FILE = "vts_token.txt"
   ```

---

### 1.2. Core Helper Functions

**Goal:** Provide simple async functions that other code can reuse.

1. **Send and receive JSON messages over WebSocket**

   ```python
   async def vts_send(ws, message: dict) -> dict:
       """Send a JSON message to VTS and return the JSON response."""
       await ws.send(json.dumps(message))
       resp_raw = await ws.recv()
       return json.loads(resp_raw)
   ```

2. **Request a new API token (only needed the first time)**

   ```python
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
   ```

3. **Load or create token helper**

   ```python
   async def vts_get_token(ws) -> str:
       """Return existing token if present, otherwise request a new one."""
       if os.path.exists(TOKEN_FILE):
           with open(TOKEN_FILE, "r", encoding="utf-8") as f:
               return f.read().strip()
       return await vts_request_token(ws)
   ```

4. **Authenticate with VTS using the token**

   ```python
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
   ```

5. **Inject parameter data (movement / expressions)**

   ```python
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
   ```

---

### 1.3. High-Level Connect & Test Function

**Goal:** A single callable function that:

* Opens the WebSocket
* Gets token, authenticates
* Sends a simple test movement (e.g. tilt head + open mouth)

1. Add a high-level function:

   ```python
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
   ```

2. Add a script entry point for manual testing:

   ```python
   if __name__ == "__main__":
       asyncio.run(vts_test_movement())
   ```

---

### 1.4. How to Test-Run the VTS Connection

1. **Start VTube Studio** and load your Live2D model.

2. In VTS settings:

   * Enable plugin / API support.
   * Confirm WebSocket port (default: `8001`).
   * Make sure parameters like `FaceAngleX` and `MouthOpen` are mapped to your model.

3. Run in a terminal:

   ```bash
   python vts_client.py
   ```

4. On first run, VTS should show a **plugin authorization popup**. Approve it.

5. Re-run the script if needed. If everything works, you should see:

   * Console: `Test movement sent to VTS.`
   * Model: head tilt and mouth movement.

If there is an error, adjust logging / print the response from VTS in `vts_send`.

---

## 2. Connect to Local LLaMA LLM

### 2.1. Environment & Imports

**Goal:** Create a Python module (e.g. `llm_client.py`) that can:

* Send a prompt to a local LLaMA model (HTTP or other API)
* Return structured JSON with emotion or movement tags

**Assumption:** The LLM is reachable via an HTTP endpoint (for example, an Ollama / llama.cpp / LM Studio style API). This can be changed later if needed.

1. Ensure Python has:

   * `requests`
   * `json` (standard library)

2. At the top of `llm_client.py`, import:

   ```python
   import json
   import requests
   ```

3. Define configurable constants:

   ```python
   LLM_URL = "http://localhost:11434/api/generate"  # adjust to your setup
   LLM_MODEL_NAME = "llama3"                        # adjust to your installed model
   ```

---

### 2.2. Define LLM Prompting Strategy

**Goal:** Make the LLM output a **simple JSON object** containing emotion/intensity based on some user text.

1. Create a function to build the system prompt:

   ```python
   def build_emotion_prompt(text: str) -> str:
       """Return a prompt asking the LLM to classify emotion for the given text."""
       return f"""
   ```

You are an emotion classifier for a VTuber avatar.

For the given text, output ONLY valid JSON with fields:

* "emotion": one of ["neutral","happy","sad","angry","surprised"]
* "intensity": a number from 0.0 to 1.0

Text: "{text}"
"""

````

---

### 2.3. Core Function: Query the LLM for Emotion

**Goal:** Send the prompt, parse JSON from the LLM output, and return a neat dict.

1. Basic LLM call function (HTTP POST style):

```python
def call_llm(prompt: str) -> str:
    """
    Send a prompt to the local LLaMA HTTP server and return its raw text response.

    Adjust the payload / keys to match the actual server.
    """
    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(LLM_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    # Adjust this if your API uses a different field name
    return data.get("response", "").strip()
````

2. Helper to extract JSON from a noisy response:

   ```python
   def extract_json_from_text(raw: str) -> dict:
       """
       Extract the first JSON object from a text string and parse it.
       Assumes there is a '{ ... }' somewhere in the text.
       """
       start = raw.find("{")
       end = raw.rfind("}")
       if start == -1 or end == -1 or end < start:
           raise ValueError("No JSON object found in LLM response")
       json_str = raw[start:end+1]
       return json.loads(json_str)
   ```

3. High-level function: get emotion for a user message:

   ```python
   def get_emotion_for_text(text: str) -> dict:
       """
       Return a dict like: {"emotion": "happy", "intensity": 0.8}
       """
       prompt = build_emotion_prompt(text)
       raw_response = call_llm(prompt)
       data = extract_json_from_text(raw_response)

       # Add simple defaults / normalization
       emotion = data.get("emotion", "neutral")
       intensity = float(data.get("intensity", 0.5))
       intensity = max(0.0, min(1.0, intensity))

       return {"emotion": emotion, "intensity": intensity}
   ```

---

### 2.4. How to Test-Run the LLM Connection

1. Make sure your **local LLaMA server** is running and matches `LLM_URL` / `LLM_MODEL_NAME`.

2. Add a simple test block at the bottom of `llm_client.py`:

   ```python
   if __name__ == "__main__":
       sample_text = "Wow, that's amazing news!"
       result = get_emotion_for_text(sample_text)
       print("Input text:", sample_text)
       print("LLM emotion result:", result)
   ```

3. Run:

   ```bash
   python llm_client.py
   ```

4. Confirm that the output is a dictionary-like structure, for example:

   ```text
   Input text: Wow, that's amazing news!
   LLM emotion result: {'emotion': 'happy', 'intensity': 0.9}
   ```

If there is a connection error, adjust `LLM_URL` and check that your LLM HTTP server is running.

If the JSON parsing fails, print out `raw_response` and adjust `extract_json_from_text` accordingly.

---

## (Optional Next Step) Combine Both Modules

Once both sections are working individually:

* Create a new script, e.g. `main_controller.py`.

* Import both modules:

  ```python
  import asyncio
  from vts_client import vts_get_token, vts_authenticate, vts_inject_parameters, VTS_URL
  from llm_client import get_emotion_for_text
  import websockets
  ```

* Add a mapping from emotion → VTS parameters.

* In an async loop, read user input text, call `get_emotion_for_text`, then send mapped parameters to VTS.

You can build this once both `vts_client.py` and `llm_client.py` pass their test runs.

```
::contentReference[oaicite:0]{index=0}
```
