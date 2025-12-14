# Abstract LLM Client Design

## Architecture Overview

The abstract LLM client provides a unified interface for multiple AI providers through aisuite while maintaining performance requirements and simplifying configuration.

### Current State Analysis

The existing `llm_client.py` already implements basic aisuite integration with:

- Environment-based provider selection (`LLM_PROVIDER`)
- Model configuration per provider (`LLM_MODEL`)
- Ollama base URL override (`OLLAMA_BASE_URL`)
- Google/Gemini provider support with API key validation

### Design Principles

1. **Single Provider Constraint**: Only one provider active at runtime
2. **Performance First**: Maintain < 500ms response requirements
3. **Configuration Simplicity**: Environment variable-based setup
4. **Provider Agnostic**: Unified interface regardless of backend
5. **Fallback Strategy**: Clear error handling for provider failures

## Provider Configuration Strategy

### Environment Variables

```bash
# Core Configuration
LLM_PROVIDER=ollama|google|openai|anthropic  # Default: ollama
LLM_MODEL=<provider-specific-model>          # Provider-dependent default

# Provider-Specific Settings
OLLAMA_BASE_URL=http://localhost:11434       # Default for Ollama
GOOGLE_API_KEY=<key>                         # Required for Google/Gemini
OPENAI_API_KEY=<key>                         # Required for OpenAI
ANTHROPIC_API_KEY=<key>                      # Required for Anthropic

# Performance Tuning
LLM_TIMEOUT=30                               # Request timeout in seconds
LLM_TEMPERATURE=0.0                          # For consistent JSON output
```

### Provider Defaults

| Provider  | Default Model    | Required Environment       |
| --------- | ---------------- | -------------------------- |
| ollama    | llama3           | OLLAMA_BASE_URL (optional) |
| google    | gemini-1.5-flash | GOOGLE_API_KEY             |
| openai    | gpt-4o-mini      | OPENAI_API_KEY             |
| anthropic | claude-3-haiku   | ANTHROPIC_API_KEY          |

## Interface Design

### Public API

The refactored client maintains the existing public interface:

```python
# Existing functions preserved
get_emotion_for_text(text: str) -> dict
build_emotion_prompt(text: str) -> str

# New configuration functions
get_current_provider() -> str
is_provider_available(provider: str) -> bool
validate_configuration() -> bool
```

### Provider Abstraction

```python
class LLMClient:
    def __init__(self):
        self._provider = None
        self._model = None
        self._client = None
        self._initialize_from_env()

    def _initialize_from_env(self) -> None:
        # Load and validate configuration
        # Initialize aisuite client
        # Set up provider-specific settings

    def call_llm(self, prompt: str) -> str:
        # Unified interface to aisuite
        # Performance monitoring
        # Error handling
```

## Configuration Management

### Provider Selection Logic

1. Check `LLM_PROVIDER` environment variable
2. Validate required API keys/endpoints exist
3. Fall back to ollama if configured provider unavailable
4. Raise configuration error if no providers available

### Validation Strategy

```python
def validate_provider_config(provider: str) -> bool:
    if provider == "ollama":
        return _check_ollama_endpoint()
    elif provider == "google":
        return bool(os.getenv("GOOGLE_API_KEY"))
    elif provider == "openai":
        return bool(os.getenv("OPENAI_API_KEY"))
    elif provider == "anthropic":
        return bool(os.getenv("ANTHROPIC_API_KEY"))
    return False
```

### Error Handling Strategy

1. **Configuration Errors**: Fail fast on startup with clear messages
2. **Runtime Errors**: Retry with exponential backoff for transient failures
3. **Provider Errors**: Log and raise with provider-specific context
4. **Timeout Errors**: Respect VTube Studio latency requirements

## Performance Considerations

### Initialization

- Lazy client initialization to minimize startup time
- Provider validation on first use rather than import time
- Connection pooling where supported by aisuite

### Runtime Performance

- Response time monitoring and logging
- Provider-specific timeout configuration
- Efficient JSON parsing and validation
- Minimal overhead abstraction layer

### Memory Management

- Single client instance reuse
- Efficient message formatting
- Cleanup of large response objects

## Migration Strategy

### Phase 1: Refactor Current Implementation

- Extract configuration logic into dedicated functions
- Improve error handling and validation
- Add provider availability checks
- Maintain backward compatibility

### Phase 2: Enhanced Abstraction

- Introduce LLMClient class for better encapsulation
- Add configuration validation at startup
- Implement provider switching capability
- Add comprehensive logging

### Phase 3: Advanced Features

- Performance monitoring and metrics
- Provider health checking
- Configuration hot-reloading
- Enhanced error recovery

## Testing Strategy

### Provider Testing

- Mock provider responses for unit tests
- Integration tests with actual providers (manual)
- Performance benchmarking against < 500ms requirement
- Configuration validation testing

### Error Scenarios

- Missing API keys
- Network connectivity issues
- Provider-specific errors
- Invalid responses and JSON parsing failures

## Security Considerations

### API Key Management

- Environment variable only (no file storage)
- Clear validation errors without key exposure
- Support for standard provider environment variables

### Network Security

- HTTPS enforcement for all providers
- Timeout configuration to prevent hanging
- Request/response size limits

## Documentation Updates

### Configuration Guide

- Complete environment variable reference
- Provider-specific setup instructions
- Troubleshooting common configuration issues

### API Reference

- Updated function signatures and return types
- Provider capability matrix
- Performance benchmarking results
