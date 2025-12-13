# LLM Client Specification

## Overview

The LLM Client provides a unified interface for multiple AI provider integrations in the VTuber emotion detection system.

## Requirements

### Provider Support

The LLM Client SHALL support the following providers:

- Ollama (local)
- Google Gemini
- OpenAI GPT
- Anthropic Claude

#### Scenario: Provider Configuration

```python
# Environment-based configuration
os.environ["LLM_PROVIDER"] = "google"
os.environ["LLM_MODEL"] = "gemini-1.5-flash"
os.environ["GOOGLE_API_KEY"] = "key"

client = LLMClient()
assert client.provider == "google"
assert client.model == "gemini-1.5-flash"
```

### Prompt Template System

The LLM Client SHALL support external prompt templates stored in `prompts/` folder.

#### Scenario: Loading Prompt Templates

```python
# prompts/emotion_system.md and prompts/emotion_user.md exist
client = LLMClient()
result = client.call_with_prompt_template("emotion", text="I'm happy!")
assert "emotion" in result
```

### Message Structure

The LLM Client SHALL support structured system and user prompts.

#### Scenario: System and User Prompts

```python
client = LLMClient()
response = client.call_llm(
    user_prompt="Analyze: I'm excited!",
    system_prompt="You are an emotion classifier."
)
assert response is not None
```

### Emotion Detection

The LLM Client SHALL provide emotion classification functionality.

#### Scenario: Emotion Classification

```python
client = LLMClient()
result = client.get_emotion_for_text("I'm so happy today!")
assert result["emotion"] in ["neutral", "happy", "sad", "angry", "surprised"]
assert 0.0 <= result["intensity"] <= 1.0
```

### Performance Requirements

The LLM Client SHALL meet real-time performance requirements.

#### Scenario: Response Time Tracking

```python
client = LLMClient()
client.call_llm("test prompt")
assert client.last_response_time is not None
assert client.is_performance_acceptable() # <500ms
```

### Backward Compatibility

The LLM Client SHALL maintain backward compatibility with existing function-based API.

#### Scenario: Legacy Function Support

```python
from llm_client import get_emotion_for_text, call_llm
result = get_emotion_for_text("I'm happy!")
assert result["emotion"] in ["neutral", "happy", "sad", "angry", "surprised"]
```
