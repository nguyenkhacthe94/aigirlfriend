# Design: Text-to-Speech Integration Architecture

## Overview

This design integrates Google Gemini's text-to-speech capabilities into the existing unified LLM response system, enabling the avatar to speak generated responses while maintaining real-time performance constraints.

## Architecture Decision

### Integration Point: LLM Client Extension

The TTS functionality will be integrated directly into the existing `LLMClient` class in `llm_client.py` rather than creating a separate module. This ensures:

- Single point of configuration and API key management
- Unified client interface for all AI operations
- Simplified dependency management
- Consistent error handling patterns

### Synchronous vs Asynchronous Design

**Decision: Synchronous TTS calls**

**Rationale:**
- Maintains the existing synchronous expression function pattern
- Prevents complex async coordination between text, expression, and audio
- Simpler error handling and debugging
- Meets the <500ms latency requirement with fast Gemini TTS models

### Audio File Management Strategy

**File Naming Convention:**
```
audio/response_{timestamp}_{session_id}.wav
```

**Storage Strategy:**
- WAV format for quality and compatibility
- Timestamp-based naming prevents conflicts
- Optional session IDs for conversation tracking
- Configurable cleanup of files older than N days

### Error Handling Philosophy

**Graceful Degradation:**
- TTS failures never block text responses or expressions
- Audio generation happens after text/expression processing
- Clear logging of TTS failures without user interruption
- Configuration flag to disable TTS entirely

## Integration Flow

```
User Input → LLM Client → Generate Response
                      ↓
         Function Calling (Expressions) ← Execute in parallel
                      ↓
         Generate TTS Audio ← Synchronous call
                      ↓
         Save Audio File ← Local storage
                      ↓
         Return Complete Response ← Text + Expression + Audio path
```

## Configuration Management

Extend existing environment variable pattern:

```bash
# Existing
GOOGLE_API_KEY="..."
LLM_MODEL="models/gemini-2.5-flash"

# New TTS Configuration
TTS_ENABLED="true"                    # Enable/disable TTS
TTS_VOICE="en-US-Casual"              # Voice selection
TTS_AUDIO_CLEANUP_DAYS="7"            # Auto-cleanup threshold
```

## Data Structures

### Response Object Extension

Current response will be extended to include audio file path:

```python
{
    "text": "Hello! How are you?",
    "expression_called": "smile",
    "audio_file": "audio/response_20241214_1234567890_abc123.wav"  # New field
}
```

### TTS Configuration Object

```python
@dataclass
class TTSConfig:
    enabled: bool = True
    voice: str = "en-US-Casual"
    speed: float = 1.0
    cleanup_days: Optional[int] = 7
    audio_format: str = "wav"
```

## Performance Considerations

### Latency Optimization

- Use google-genai's synchronous TTS endpoint
- Pre-validated voice and model configurations
- Minimal audio post-processing
- Direct file writing without streaming

### Resource Management

- Automatic cleanup of old audio files
- WAV format balance between quality and size
- Session-based audio file organization
- Optional audio file compression

## Testing Strategy

### Manual Testing Focus

Following project conventions, testing will be manual and real-world focused:

1. **Audio Quality Testing**: Human evaluation of generated speech
2. **Latency Testing**: Measure TTS impact on overall response time
3. **Integration Testing**: Verify audio-visual synchronization
4. **Error Testing**: TTS failures and network interruptions

### Development Scripts

Create debugging scripts in `scripts/debug/`:
- `debug_tts_generation.py` - Test TTS in isolation
- `debug_audio_cleanup.py` - Test file management
- `debug_tts_integration.py` - Test full integration flow