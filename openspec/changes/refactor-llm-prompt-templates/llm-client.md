# LLM Client Specification Delta

## MODIFIED Requirements

### Prompt Template System

The LLM Client SHALL support external prompt templates stored in `prompts/` folder as Markdown files.

#### Scenario: Template-based Emotion Detection

```python
# prompts/emotion_system.md contains system prompt
# prompts/emotion_user.md contains user prompt template with {text} placeholder
client = LLMClient()
result = client.call_with_prompt_template("emotion", text="I'm excited!")
assert "emotion" in json.loads(result)
```

#### Scenario: Prompt Loading

```python
client = LLMClient()
system_prompt = client._load_prompt("emotion_system")
user_prompt = client._load_prompt("emotion_user")
assert "emotion classifier" in system_prompt.lower()
assert "{text}" in user_prompt
```

### Message Structure

The LLM Client SHALL accept separate system and user prompts in call_llm method.

#### Scenario: Structured Prompt Calls

```python
client = LLMClient()
response = client.call_llm(
    user_prompt="Analyze the emotion in: I'm thrilled!",
    system_prompt="You are a precise emotion classifier."
)
assert response is not None
```

## REMOVED Requirements

### Gemini Model Recommendations

~~The LLM Client SHALL provide Gemini-specific model recommendations based on performance requirements.~~

#### ~~Scenario: Model Recommendations~~

```python
# REMOVED - No longer supported
# model = get_gemini_model_recommendation(0.2)  # Fast response
# assert model == "gemini-1.5-flash-8b"
```

### Gemini Configuration Helpers

~~The LLM Client SHALL provide helper functions for Gemini configuration.~~

#### ~~Scenario: Gemini Configuration~~

```python
# REMOVED - No longer supported
# client = configure_gemini("flash")
# assert client.provider == "google"
# assert is_gemini_configured() == bool(os.getenv("GOOGLE_API_KEY"))
```

## ADDED Requirements

### Template Method

The LLM Client SHALL provide a method to call LLM using prompt templates with variable substitution.

#### Scenario: Template Variable Substitution

```python
client = LLMClient()
# emotion_user.md contains: "Analyze: {text}"
result = client.call_with_prompt_template("emotion", text="I'm happy!")
# Should substitute {text} with "I'm happy!" in the user prompt
```
