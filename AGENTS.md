# AGENTS.md

AI-powered VTuber controller that uses LLM emotion detection to drive Live2D avatar expressions in real-time.

<!-- PROJECT_OVERVIEW:START -->

## Project Overview

This project connects an AI language model with VTube Studio to create an emotion-responsive Live2D avatar. Text input is analyzed for emotional content, which then drives facial expressions and movements in real-time through VTube Studio's WebSocket API.

**Key Components:**

- `vts_client.py` - VTube Studio WebSocket API client (authentication, parameter injection)
- `llm_client.py` - LLM emotion detection client
- `main.py` - Main orchestration loop
- `vts_movement.py` - Movement and animation utilities
- `ai_bot.py` - Bot integration layer
- `scripts/` - Development-only debugging, helper, and sanity test scripts (never use in production)
<!-- PROJECT_OVERVIEW:END -->

<!-- BUILD_TEST:START -->

## Build and Test Commands

```bash
# Run the main application
python main.py

# Test VTube Studio connection
python scripts/test_vts_connection.py

# Test LLM emotion detection
python scripts/test_llm_emotion.py

# Test movement system
python scripts/test_movement_system.py

# No formal test suite - manual testing preferred for real-time interactivity
```

**Note:** All debugging, helper, and sanity test scripts are located in the `scripts/` folder and are intended for development use only. These scripts should never be used in production environments.

<!-- BUILD_TEST:END -->

<!-- ARCHITECTURE:START -->

## Python Architecture Guidelines

### Module Organization Philosophy

**CRITICAL:** Prioritize deep, cohesive module implementation over scattered functionality.

Each module should be:

- **Self-contained** - All related functionality in one place
- **Deep** - Rich, comprehensive interfaces with minimal surface area
- **Minimal coupling** - Clear, narrow contracts between modules

### Code Style

- **PEP 8 compliance** with snake_case for functions/variables, UPPER_SNAKE_CASE for constants
- **Type hints required** for all public functions (Python 3.10+ syntax)
- **Docstrings** - Use Google-style docstrings for all public functions and classes
- **Async-first** - Use `async`/`await` for I/O operations
- **Simple > Complex** - Optimize for readability and speed over abstraction
- **Minimal error handling** - Fast failure over defensive programming (real-time constraints)

### Module Design Patterns

#### 1. Client Modules (`vts_client.py`, `llm_client.py`)

**Structure:**

```python
# Module-level constants at top
API_URL = "..."
DEFAULT_TIMEOUT = 30

# Private helper functions (prefix with _)
def _parse_response(data: dict) -> dict:
    ...

# Public API functions (comprehensive, well-documented)
async def connect(url: str) -> Connection:
    """Establish connection with full lifecycle management."""
    ...

async def authenticate(conn: Connection, token: str) -> bool:
    """Authenticate and handle token persistence."""
    ...
```

**Requirements:**

- Single responsibility per module
- All related operations in one file (no splitting connection logic across files)
- State management encapsulated within module
- Public API should be narrow but powerful

#### 2. Orchestration (`main.py`)

**Structure:**

```python
# Minimal imports - only what's needed
from vts_client import VTSClient
from llm_client import EmotionDetector

# Configuration at module level
EMOTION_MAP = {...}

async def main():
    """Main event loop with clear lifecycle."""
    ...
```

**Requirements:**

- Thin orchestration layer - delegate to modules
- No business logic here - only coordination
- Clear lifecycle management (setup, loop, cleanup)

### Deep Module Example

**Good** - Deep, cohesive module:

```python
# vts_client.py
class VTSClient:
    """Complete VTube Studio WebSocket client with authentication and parameter control."""

    def __init__(self, url: str = "ws://localhost:8001"):
        self._url = url
        self._ws = None
        self._token = None

    async def connect(self) -> None:
        """Establish WebSocket connection and authenticate."""
        ...

    async def set_parameters(self, params: dict[str, float]) -> None:
        """Set multiple avatar parameters atomically."""
        ...

    async def _request_token(self) -> str:
        """Request new auth token (private helper)."""
        ...
```

**Bad** - Scattered across files:

```python
# vts_connection.py
async def connect(url): ...

# vts_auth.py
async def authenticate(ws, token): ...

# vts_params.py
async def set_params(ws, params): ...
```

### Testing Guidelines

- **Manual testing only** - Real-time interactivity requires human validation
- **Fast iteration** over test coverage
- Test in VTube Studio with actual avatar
- Verify <500ms latency for emotion detection
- **All debugging, helper, and sanity test scripts must be placed in the `scripts/` folder**
- **Scripts in the `scripts/` folder are development-only and should never be used in production**
<!-- ARCHITECTURE:END -->

<!-- DOMAIN_CONTEXT:START -->

## Domain-Specific Context

### Emotion System

**Supported Emotions:**

- `neutral`, `happy`, `sad`, `angry`, `surprised`

**LLM Response Format:**

```json
{
  "emotion": "happy",
  "intensity": 0.8
}
```

**Intensity Scaling:**

- Range: 0.0 (subtle) to 1.0 (maximum)
- Applied multiplicatively to parameter values
- Example: `MouthOpen: 0.5 * intensity`

### VTube Studio Parameters

**Common Parameters** (normalized 0.0-1.0):

- `FaceAngleX`, `FaceAngleY`, `FaceAngleZ` - Head rotation
- `MouthOpen` - Mouth opening (0=closed, 1=fully open)
- `EyeOpenLeft`, `EyeOpenRight` - Eye openness
- Custom parameters from your Live2D model

**Parameter Injection:**

```python
params = {
    "FaceAngleX": 5.0,
    "MouthOpen": 0.8,
    "EyeOpenLeft": 0.9
}
await vts_client.set_parameters(params)
```

<!-- DOMAIN_CONTEXT:END -->

<!-- IMPLEMENTATION_GUIDE:START -->

## Implementation Guide

This section provides detailed step-by-step instructions for implementing the VTube Studio and LLM integration modules.

**Important:** All debugging, helper, and sanity test scripts must be placed in the `scripts/` folder. These scripts are development-only and should never be used in production environments.

### VTube Studio Client Implementation (`vts_client.py`)

#### Environment & Imports

Ensure Python has these packages: `websockets`, `asyncio`, `json`, `os`

```python
import asyncio
import json
import os
import websockets

# Module constants
VTS_URL = "ws://localhost:8001"
PLUGIN_NAME = "Llama Live2D Controller"
PLUGIN_DEV = "YourName"
TOKEN_FILE = "vts_token.txt"
```

#### Core Helper Functions

**1. Send and receive JSON messages:**

```python
async def vts_send(ws, message: dict) -> dict:
    """Send a JSON message to VTS and return the JSON response."""
    await ws.send(json.dumps(message))
    resp_raw = await ws.recv()
    return json.loads(resp_raw)
```

**2. Request authentication token:**

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

**3. Load or create token:**

```python
async def vts_get_token(ws) -> str:
    """Return existing token if present, otherwise request a new one."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return await vts_request_token(ws)
```

**4. Authenticate with VTS:**

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

**5. Inject parameter data:**

```python
async def vts_inject_parameters(ws, params: dict, face_found: bool = True) -> None:
    """
    Inject Live2D parameter values.

    Args:
        ws: WebSocket connection
        params: dict like {"FaceAngleX": 10.0, "MouthOpen": 0.8}
        face_found: Whether face tracking is active
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

#### High-Level Test Function

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

if __name__ == "__main__":
    asyncio.run(vts_test_movement())
```

**Note:** Save this test code as `scripts/test_vts_connection.py` for development testing only.

#### Testing VTS Connection

1. Start VTube Studio and load your Live2D model
2. In VTS settings:
   - Enable plugin/API support
   - Confirm WebSocket port (default: 8001)
   - Ensure parameters like `FaceAngleX` and `MouthOpen` are mapped
3. Run: `python scripts/test_vts_connection.py`
4. On first run, approve the plugin authorization popup in VTS
5. Verify console output: "Test movement sent to VTS."
6. Confirm model shows head tilt and mouth movement

### LLM Client Implementation (`llm_client.py`)

#### Environment & Imports

Ensure Python has: `requests`, `json`

```python
import json
import requests

# Module constants
LLM_URL = "http://localhost:11434/api/generate"  # adjust to your setup
LLM_MODEL_NAME = "llama3"                        # adjust to your installed model
```

#### Prompting Strategy

```python
def build_emotion_prompt(text: str) -> str:
    """Return a prompt asking the LLM to classify emotion for the given text."""
    return f"""
You are an emotion classifier for a VTuber avatar.

For the given text, output ONLY valid JSON with fields:

* "emotion": one of ["neutral","happy","sad","angry","surprised"]
* "intensity": a number from 0.0 to 1.0

Text: "{text}"
"""
```

#### Core Functions

**1. Query LLM:**

```python
def call_llm(prompt: str) -> str:
    """
    Send a prompt to the local LLaMA HTTP server and return its raw text response.

    Adjust the payload/keys to match the actual server.
    """
    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(LLM_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "").strip()
```

**2. Extract JSON from response:**

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

**3. Get emotion for text:**

```python
def get_emotion_for_text(text: str) -> dict:
    """
    Return a dict like: {"emotion": "happy", "intensity": 0.8}
    """
    prompt = build_emotion_prompt(text)
    raw_response = call_llm(prompt)
    data = extract_json_from_text(raw_response)

    # Add simple defaults/normalization
    emotion = data.get("emotion", "neutral")
    intensity = float(data.get("intensity", 0.5))
    intensity = max(0.0, min(1.0, intensity))

    return {"emotion": emotion, "intensity": intensity}
```

#### Testing LLM Connection

```python
if __name__ == "__main__":
    sample_text = "Wow, that's amazing news!"
    result = get_emotion_for_text(sample_text)
    print("Input text:", sample_text)
    print("LLM emotion result:", result)
```

**Note:** Save this test code as `scripts/test_llm_emotion.py` for development testing only.

Run: `python scripts/test_llm_emotion.py`

Expected output:

```
Input text: Wow, that's amazing news!
LLM emotion result: {'emotion': 'happy', 'intensity': 0.9}
```

### Prompt Management Guidelines

**CRITICAL:** All LLM prompts MUST be stored in the `prompts/` folder as Markdown files.

#### Prompt Template Example

**prompts/emotion_system.md:**

```markdown
# Emotion Detection System Prompt

You are a precise emotion classifier for a VTuber avatar system.

## Response Requirements

- Respond ONLY with valid JSON containing emotion and intensity fields
- No additional text, explanations, or formatting

## Available Emotions

neutral, happy, sad, angry, surprised

## Intensity Scale

0.0-1.0 where 0.0 = neutral, 1.0 = maximum intensity
```

**Rules:**

1. **Never hardcode prompts in Python code** - Always use template files
2. **Use descriptive template names** - `emotion_`, `conversation_`, `analysis_`
3. **Include placeholder documentation** - Document all `{variable}` substitutions
4. **Version control prompts** - Templates are part of the codebase
5. **Test prompt changes independently** - Verify templates before code integration

### Combining Both Modules (`main.py`)

Once both modules work individually:

```python
import asyncio
import websockets
from vts_client import vts_get_token, vts_authenticate, vts_inject_parameters, VTS_URL
from llm_client import get_emotion_for_text

# Mapping from emotion to VTS parameters
EMOTION_MAP = {
    "neutral": {"FaceAngleX": 0.0, "MouthOpen": 0.0, "EyeOpenLeft": 1.0, "EyeOpenRight": 1.0},
    "happy": {"FaceAngleX": 5.0, "MouthOpen": 0.5, "EyeOpenLeft": 0.8, "EyeOpenRight": 0.8},
    "sad": {"FaceAngleX": -10.0, "MouthOpen": 0.0, "EyeOpenLeft": 0.6, "EyeOpenRight": 0.6},
    "angry": {"FaceAngleX": 0.0, "MouthOpen": 0.2, "EyeOpenLeft": 0.7, "EyeOpenRight": 0.7},
    "surprised": {"FaceAngleX": 0.0, "MouthOpen": 1.0, "EyeOpenLeft": 1.0, "EyeOpenRight": 1.0}
}

async def main():
    """Main event loop combining LLM emotion detection and VTS control."""
    print("Connecting to VTube Studio...")
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
            emotion_data = get_emotion_for_text(user_input)
            emotion = emotion_data["emotion"]
            intensity = emotion_data["intensity"]
            print(f"Detected emotion: {emotion} (intensity: {intensity})")

            # Get parameters for the emotion
            params = EMOTION_MAP.get(emotion, EMOTION_MAP["neutral"]).copy()

            # Apply intensity scaling
            if "MouthOpen" in params:
                params["MouthOpen"] *= intensity

            # Inject into VTube Studio
            await vts_inject_parameters(ws, params)
            print(f"Applied {emotion} expression to avatar.")

if __name__ == "__main__":
    asyncio.run(main())
```

<!-- IMPLEMENTATION_GUIDE:END -->

<!-- SECURITY_CONFIG:START -->

## Security and Configuration

### Environment Variables

```bash
# LLM Provider Configuration
export LLM_PROVIDER="ollama"  # ollama (default), google, openai, anthropic
export LLM_MODEL="llama3"     # provider-specific model name

# Provider-Specific API Keys
export GOOGLE_API_KEY="your-google-api-key"      # for Gemini
export OPENAI_API_KEY="your-openai-api-key"      # for OpenAI
export ANTHROPIC_API_KEY="your-anthropic-api-key" # for Anthropic

# Optional Performance Tuning
export OLLAMA_BASE_URL="http://localhost:11434"  # custom Ollama endpoint
export LLM_TIMEOUT="30"                          # request timeout
export LLM_TEMPERATURE="0.0"                     # for consistent JSON

# VTube Studio
export VTS_URL="ws://localhost:8001"             # VTS WebSocket URL
```

### Token Persistence

- VTS authentication token stored in `vts_token.txt`
- First connection requires manual approval in VTube Studio
- Token reused on subsequent runs
- API keys only loaded from environment variables (never stored in files)

### Provider Setup

See [docs/LLM_CLIENT.md](docs/LLM_CLIENT.md) for detailed configuration instructions for each provider.

<!-- SECURITY_CONFIG:END -->

<!-- PERFORMANCE:START -->

## Performance Constraints

**Critical Requirements:**

- **<500ms latency** for LLM emotion detection
- Real-time responsiveness for smooth avatar animation
- Async I/O mandatory for WebSocket operations
- Minimal dependencies to reduce startup time
<!-- PERFORMANCE:END -->

<!-- COMMON_TASKS:START -->

## Common Tasks

### Adding a New Emotion

1. Update `EMOTION_MAP` in `main.py`:

```python
EMOTION_MAP["excited"] = {
    "FaceAngleX": 10.0,
    "MouthOpen": 0.9,
    "EyeOpenLeft": 1.0
}
```

2. Update LLM prompt in `llm_client.py`:

```python
emotion_list = '["neutral","happy","sad","angry","surprised","excited"]'
```

### Adding Custom VTS Parameters

1. Find parameter name in VTube Studio API
2. Add to emotion mapping with appropriate value
3. Test with actual avatar to verify visual effect

### Switching LLM Providers

Modify `llm_client.py` configuration:

```python
# Using aisuite for multiple providers
import aisuite as ai
client = ai.Client()

response = client.chat.completions.create(
    model="openai:gpt-4",  # or "anthropic:claude-3-opus"
    messages=[{"role": "user", "content": prompt}]
)
```

<!-- COMMON_TASKS:END -->

<!-- GIT_WORKFLOW:START -->

## Git Workflow

- Direct commits to `master` - no branching overhead
- Commit messages: Short, imperative mood ("Add emotion X", "Fix parameter scaling")
- Fast iteration prioritized over formal process
<!-- GIT_WORKFLOW:END -->

<!-- DEPENDENCIES:START -->

## External Dependencies

### Python Packages

See `requirements.txt`:

- `websockets` - VTS WebSocket client
- `requests` - HTTP client for API calls
- `asyncio` - Built-in async support
- `aisuite` - Unified LLM provider interface

### Required Services

1. **VTube Studio**

   - Must be running before starting this app
   - WebSocket API enabled (Settings → General → Enable API)
   - Port 8001 (default)

2. **LLM Provider**
   - API key configured in environment
   - Model supports JSON output
   - Sub-500ms response time
   <!-- DEPENDENCIES:END -->

<!-- TROUBLESHOOTING:START -->

## Troubleshooting

### VTube Studio Connection Failed

```bash
# Check if VTube Studio is running
lsof -i :8001

# Verify API is enabled in VTube Studio settings
```

### Authentication Required

- Click "Allow" in VTube Studio when prompted
- Token saved to `vts_token.txt` for future use
- If authentication fails after denying the plugin request, delete `vts_token.txt` and try again

### Slow Emotion Detection

- Check LLM provider latency
- Consider local model (Ollama) for lower latency
- Verify network connection

### Parameter Not Working

- Verify parameter name in VTube Studio API
- Check Live2D model supports the parameter
- Test with VTube Studio's parameter panel first
<!-- TROUBLESHOOTING:END -->

<!-- OPENSPEC:START -->

## OpenSpec Integration

For architectural changes, feature proposals, or major refactoring:

**Always consult** `@/openspec/AGENTS.md` when:

- Creating proposals for new features or breaking changes
- Planning architecture modifications
- Adding new capabilities to the emotion or animation system
- Making performance or security improvements

The OpenSpec workflow provides structured change management for this project.

<!-- OPENSPEC:END -->
