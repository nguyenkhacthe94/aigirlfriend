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
<!-- PROJECT_OVERVIEW:END -->

<!-- BUILD_TEST:START -->

## Build and Test Commands

```bash
# Run the main application
python main.py

# Test VTube Studio connection
python vts_client.py

# Test LLM emotion detection
python llm_client.py

# Test movement system
# No formal test suite - manual testing preferred for real-time interactivity
```

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

- **Fast iteration** over test coverage
- Test in VTube Studio with actual avatar
- Verify <500ms latency for emotion detection
<!-- ARCHITECTURE:END -->

<!-- DOMAIN_CONTEXT:START -->

## Domain-Specific Contexttest coverage

- Test in VTube Studio with actual avatar
- Verify <500ms latency for emotion detection

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
await vts_client.set_parameters(params)
```

<!-- DOMAIN_CONTEXT:END -->

<!-- SECURITY_CONFIG:START -->

## Security and Configuration

### Environment Variables

````bash
# Required
export LLM_API_KEY="your-api-key-here"

# Optional
- VTS authentication token stored in `vts_token.txt`
- First connection requires manual approval in VTube Studio
- Token reused on subsequent runs
<!-- SECURITY_CONFIG:END -->

<!-- PERFORMANCE:START -->
## Performance Constraints

- VTS authentication token stored in `vts_token.txt`
- First connection requires manual approval in VTube Studio
- Token reused on subsequent runs
- Real-time responsiveness for smooth avatar animation
- Async I/O mandatory for WebSocket operations
- Minimal dependencies to reduce startup time
<!-- PERFORMANCE:END -->

<!-- COMMON_TASKS:START -->
## Common Tasks
- **<500ms latency** for LLM emotion detection
- Real-time responsiveness for smooth avatar animation
- Async I/O mandatory for WebSocket operations
- Minimal dependencies to reduce startup time

## Common Tasks

### Adding a New Emotion

1. Update `EMOTION_MAP` in `main.py`:

```python
EMOTION_MAP["excited"] = {
    "FaceAngleX": 10.0,
    "MouthOpen": 0.9,
    "EyeOpenLeft": 1.0
}
````

2. Update LLM prompt in `llm_client.py`:

```python
emotion_list = '["neutral","happy","sad","angry","surprised","excited"]'
```

### Adding Custom VTS Parameters

1. Find parameter name in VTube Studio API
2. Add to emotion mapping with appropriate value
3. Test with actual avatar to verify visual effect

### Switching LLM Providers

```
Modify `llm_client.py` configuration:
    messages=[{"role": "user", "content": prompt}]
```

<!-- COMMON_TASKS:END -->

<!-- GIT_WORKFLOW:START -->

## Git Workflow

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

- `requests` - HTTP client for API calls
- `asyncio` - Built-in async support
- `aisuite` - Unified LLM provider interface
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
- Verify parameter name in VTube Studio API
- Check Live2D model supports the parameter
- Test with VTube Studio's parameter panel first

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
