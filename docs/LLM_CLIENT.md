# Abstract LLM Client Documentation

## Overview

The abstract LLM client provides a unified interface for multiple AI providers through aisuite while maintaining performance requirements and simplifying provider switching for the VTuber emotion detection system.

## Quick Start

### Basic Usage (Ollama - Default)

```bash
# No configuration needed for Ollama on localhost
export LLM_PROVIDER=ollama  # optional, this is the default
python main.py
```

### Google Gemini Configuration

```bash
export LLM_PROVIDER=google
export GOOGLE_API_KEY=your_api_key_here
export LLM_MODEL=gemini-1.5-flash  # optional, this is the default
python main.py
```

### OpenAI Configuration

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_api_key_here
export LLM_MODEL=gpt-4o-mini  # optional, this is the default
python main.py
```

### Anthropic Configuration

```bash
export LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your_api_key_here
export LLM_MODEL=claude-3-haiku  # optional, this is the default
python main.py
```

## Environment Variables Reference

| Variable            | Default                  | Description                                          |
| ------------------- | ------------------------ | ---------------------------------------------------- |
| `LLM_PROVIDER`      | `ollama`                 | AI provider (ollama, google, openai, anthropic)      |
| `LLM_MODEL`         | Provider-specific        | Model name for the selected provider                 |
| `LLM_TIMEOUT`       | `30`                     | Request timeout in seconds                           |
| `LLM_TEMPERATURE`   | `0.0`                    | Temperature for consistent JSON output               |
| `OLLAMA_BASE_URL`   | `http://localhost:11434` | Ollama server URL                                    |
| `GOOGLE_API_KEY`    | None                     | Google/Gemini API key (required for google provider) |
| `OPENAI_API_KEY`    | None                     | OpenAI API key (required for openai provider)        |
| `ANTHROPIC_API_KEY` | None                     | Anthropic API key (required for anthropic provider)  |

## Provider-Specific Configuration

### Ollama

**Default Model**: `llama3`
**Required Environment**: None (uses localhost by default)
**Optional Environment**: `OLLAMA_BASE_URL` for custom endpoints

```bash
# Custom Ollama endpoint
export OLLAMA_BASE_URL=http://192.168.1.100:11434
export LLM_MODEL=mistral  # if you have mistral installed
```

### Google Gemini

**Default Model**: `gemini-1.5-flash` (optimized for speed)
**Required Environment**: `GOOGLE_API_KEY`
**Available Models**: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-1.5-flash-8b`

```bash
export GOOGLE_API_KEY=your_api_key
export LLM_MODEL=gemini-1.5-pro  # for higher quality (slower)
```

**Performance Recommendations**:

- `gemini-1.5-flash-8b`: Fastest, <300ms typical
- `gemini-1.5-flash`: Balanced, <500ms typical
- `gemini-1.5-pro`: Highest quality, may exceed 500ms

### OpenAI

**Default Model**: `gpt-4o-mini` (cost-optimized)
**Required Environment**: `OPENAI_API_KEY`
**Available Models**: `gpt-4o-mini`, `gpt-4o`, `gpt-3.5-turbo`

### Anthropic

**Default Model**: `claude-3-haiku` (speed-optimized)
**Required Environment**: `ANTHROPIC_API_KEY`
**Available Models**: `claude-3-haiku`, `claude-3-sonnet`, `claude-3-opus`

## Programming Interface

### Backward Compatibility

All existing code continues to work unchanged:

```python
from llm_client import get_emotion_for_text

result = get_emotion_for_text("I'm so happy today!")
print(result)  # {"emotion": "happy", "intensity": 0.8}
```

### Advanced Usage with LLMClient Class

```python
from llm_client import LLMClient, configure_gemini

# Create provider-specific clients
ollama_client = LLMClient(provider="ollama", model="llama3")
gemini_client = configure_gemini("flash")  # Optimized for speed

# Use specific client
result = gemini_client.get_emotion_for_text("Amazing news!")
print(f"Response time: {gemini_client.last_response_time:.3f}s")
print(f"Performance OK: {gemini_client.is_performance_acceptable()}")
```

### Provider Validation

```python
from llm_client import validate_provider_config, is_gemini_configured

# Check if providers are configured
print("Ollama:", validate_provider_config("ollama"))
print("Gemini:", is_gemini_configured())
print("OpenAI:", validate_provider_config("openai"))
```

## Performance Optimization

### VTuber Real-time Requirements

The system maintains the <500ms response time requirement:

- Response time monitoring built-in
- Performance validation after each request
- Provider-specific optimizations

### Gemini Optimization

```python
from llm_client import get_gemini_model_recommendation

# Get recommended model for your latency requirements
model = get_gemini_model_recommendation(max_latency=0.3)
print(f"Recommended Gemini model: {model}")
```

### Provider Selection for Performance

| Provider               | Typical Latency | Notes                             |
| ---------------------- | --------------- | --------------------------------- |
| Ollama (local)         | <200ms          | Fastest, requires local setup     |
| Google Gemini Flash    | <400ms          | Good balance of speed and quality |
| OpenAI GPT-4o-mini     | <600ms          | May exceed 500ms occasionally     |
| Anthropic Claude Haiku | <500ms          | Reliable performance              |

## Troubleshooting

### Configuration Errors

**Error**: "Google/Gemini provider requires GOOGLE_API_KEY"
**Solution**: Set your Google API key:

```bash
export GOOGLE_API_KEY=your_key_here
```

**Error**: "Ollama provider configuration error"
**Solution**: Check Ollama is running and URL is correct:

```bash
curl http://localhost:11434/api/tags
```

**Error**: "LLM provider 'provider_name' error: timeout"
**Solution**: Increase timeout or check network connectivity:

```bash
export LLM_TIMEOUT=60
```

### Performance Issues

**Problem**: Response time >500ms
**Solutions**:

1. Use faster models (e.g., `gemini-1.5-flash-8b`)
2. Use local Ollama provider
3. Check network latency

**Problem**: Inconsistent JSON responses
**Solution**: Temperature is automatically set to 0.0 for consistent output

### API Key Management

**Problem**: API key not found
**Solutions**:

1. Set environment variable in your shell profile
2. Use a `.env` file with python-dotenv
3. Set in your deployment environment

```bash
# Add to ~/.bashrc or ~/.zshrc
export GOOGLE_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here
```

## Migration Guide

### From Old Implementation

The new implementation maintains 100% backward compatibility. No code changes required.

### Adding New Providers

If you're switching providers:

1. Set new environment variables
2. Restart application
3. Test with validation functions

### Performance Testing

```python
from llm_client import LLMClient

client = LLMClient()
result = client.get_emotion_for_text("Test message")
print(f"Response time: {client.last_response_time:.3f}s")

if not client.is_performance_acceptable():
    print("⚠️ Performance issue detected")
```

## Security Considerations

- API keys are only loaded from environment variables
- No API keys are stored in files or logged
- Timeout prevents hanging requests
- Provider validation prevents misconfiguration

## Testing

Use the provided test script:

```bash
python scripts/test_abstract_llm_client.py
```

This validates:

- Provider configuration
- API connectivity
- Emotion detection functionality
- Performance requirements
