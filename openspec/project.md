# Project Context

## Purpose

AI-powered VTuber controller that uses LLM emotion detection to drive Live2D avatar expressions in real-time.

## Tech Stack

- **Python 3.10+** - Core language
- **websockets** - VTube Studio WebSocket API client
- **requests** - HTTP client for API calls
- **asyncio** - Async WebSocket handling
- **aisuite** - unified API for working with multiple Generative AI providers
- **VTube Studio** - Live2D rendering engine (WebSocket on ws://localhost:8001)

## Project Conventions

### Code Style

- Simple, direct Python - optimize for speed over abstraction
- Minimal error handling
- Inline comments only when logic is non-obvious
- Module-level constants in UPPER_SNAKE_CASE
- Functions and variables in snake_case

### Architecture Patterns

- **Modular design**: `vts_client.py` (VTube Studio), `llm_client.py` (LLM), `main.py` (orchestration)
- **Async-first**: Use async/await for WebSocket I/O
- **Simple mappings**: Direct emotion→parameter dictionaries
- **File-based persistence**: Token storage in `vts_token.txt`

### Testing Strategy

Manual testing only - fast iteration over test coverage

### Git Workflow

Direct commits to master - no branching overhead

## Domain Context

- **Emotions**: neutral, happy, sad, angry, surprised
- **VTS Parameters**: FaceAngleX, MouthOpen, EyeOpenLeft/Right (normalized 0.0-1.0)
- **LLM Response**: JSON with `{"emotion": str, "intensity": float}`
- **Intensity scaling**: Multiply parameter values by intensity for dynamic range

## Important Constraints

- **Performance critical**: Real-time responsiveness required (<500ms LLM response)
- **Minimal dependencies**: Keep it lean
- **API key security**: Use environment variables

## External Dependencies

- VTube Studio must be running on port 8001
- Manual authentication approval required on first VTS connection
