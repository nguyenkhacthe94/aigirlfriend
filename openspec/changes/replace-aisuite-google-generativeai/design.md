# Design Document: aisuite to google-generativeai Migration

## Overview

This document outlines the technical design for replacing aisuite with direct google-generativeai usage while maintaining the existing API contract.

## Architecture Comparison

### Current Architecture (aisuite)

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│ main.py     │───▶│ LLMClient    │───▶│ aisuite.Client │───▶│ Gemini API  │
│             │    │ (wrapper)    │    │ (abstraction)  │    │             │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                         │
                         ▼
                   ┌──────────────┐
                   │ Expression   │
                   │ Functions    │
                   └──────────────┘
```

### Proposed Architecture (google-generativeai)

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ main.py     │───▶│ LLMClient    │───▶│ Gemini API  │
│             │    │ (direct)     │    │             │
└─────────────┘    └──────────────┘    └─────────────┘
                         │
                         ▼
                   ┌──────────────┐
                   │ Expression   │
                   │ Functions    │
                   └──────────────┘
```

## Key Design Decisions

### 1. API Compatibility

Maintain the exact same public interface:

```python
# Public API remains unchanged
class LLMClient:
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None)
    def call_llm(self, user_prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]
    @property def provider(self) -> str
    @property def model(self) -> str
    @property def last_response_time(self) -> Optional[float]
    def is_performance_acceptable(self) -> bool
```

### 2. Configuration Strategy

Keep existing environment variable system but simplify internally:

```python
# Environment Variables (unchanged)
GOOGLE_API_KEY          # Required for Google/Gemini
LLM_MODEL              # Default: "gemini-1.5-flash"
LLM_TIMEOUT            # Default: 30 seconds
LLM_TEMPERATURE        # Default: 0.75

# Remove unused provider variables
# LLM_PROVIDER - Always "google" now
# OLLAMA_BASE_URL, OPENAI_API_KEY, ANTHROPIC_API_KEY - No longer needed
```

### 3. Function Calling Implementation

#### Current (aisuite)

```python
response = client.chat.completions.create(
    model=self._get_model_string(),
    messages=messages,
    tools=EXPRESSION_TOOLS,
    max_turns=2,
    temperature=self._temperature,
    max_tokens=300,
)
```

#### Proposed (google-generativeai)

```python
import google.generativeai as genai
from google.genai import types

# Configure client
client = genai.Client(api_key=self._google_api_key)

# Convert expression functions to Google tools
tools = [types.FunctionDeclaration.from_callable(client=client, callable=func)
         for func in EXPRESSION_TOOLS]

response = client.models.generate_content(
    model=self._model,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=tools,
        temperature=self._temperature,
        max_tokens=300
    )
)
```

### 4. Response Processing Design

Maintain the same response structure:

```python
{
    "text_response": str,           # LLM conversational response
    "expression_called": str | None, # Name of function called
    "intermediate_messages": list    # Full conversation history
}
```

#### Implementation Strategy

```python
def _parse_unified_response(self, response) -> Dict[str, Any]:
    """Parse google-generativeai response maintaining aisuite format."""
    result = {
        "text_response": "",
        "expression_called": None,
        "intermediate_messages": [],
    }

    # Extract text response
    result["text_response"] = response.text or ""

    # Check for function calls
    if hasattr(response, 'function_calls') and response.function_calls:
        result["expression_called"] = response.function_calls[0].name
        # Execute function automatically (Google SDK feature)

    return result
```

### 5. Error Handling Strategy

Map Google-specific errors to consistent format:

```python
def _handle_api_errors(self, error: Exception) -> Exception:
    """Convert Google API errors to consistent format."""
    if isinstance(error, genai.types.GenerationError):
        return RuntimeError(f"Generation failed: {error}")
    elif isinstance(error, genai.types.APIError):
        return ConnectionError(f"API error: {error}")
    else:
        return Exception(f"LLM request failed: {error}")
```

## Implementation Details

### Class Structure

```python
class LLMClient:
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        self._provider = "google"  # Always Google now
        self._model = model or os.getenv("LLM_MODEL", "gemini-1.5-flash")
        self._google_api_key = os.getenv("GOOGLE_API_KEY")
        self._client = self._create_client()

    def _create_client(self) -> genai.Client:
        """Create Google GenerativeAI client."""
        if not self._google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable required")
        return genai.Client(api_key=self._google_api_key)
```

### Function Declaration Conversion

```python
def _convert_expression_functions(self) -> List[types.FunctionDeclaration]:
    """Convert expression functions to Google FunctionDeclarations."""
    return [
        types.FunctionDeclaration.from_callable(
            client=self._client,
            callable=func
        ) for func in EXPRESSION_TOOLS
    ]
```

## Migration Strategy

### Phase 1: Side-by-Side Implementation

- Create GoogleLLMClient class alongside existing LLMClient
- Implement all methods with google-generativeai
- Comprehensive testing

### Phase 2: API Replacement

- Replace LLMClient implementation with GoogleLLMClient
- Update imports and dependencies
- Run integration tests

### Phase 3: Cleanup

- Remove aisuite dependencies
- Clean up unused code
- Update documentation

## Risk Mitigation

### Backward Compatibility

- Maintain exact same public API
- Keep same response format
- Preserve configuration system

### Performance

- Direct API calls should be faster
- Remove wrapper overhead
- Monitor latency improvements

### Reliability

- Reduce dependency count
- Simpler error paths
- Better error messages

## Testing Strategy

### Unit Tests

- Test all public methods
- Mock Google API responses
- Validate response format compatibility

### Integration Tests

- End-to-end expression calling
- Performance comparisons
- Error handling scenarios

### Validation Tests

- Compare outputs with current implementation
- Verify function calling works identically
- Performance benchmarks

## Performance Expectations

- **Latency**: Equal or better than current (remove aisuite overhead)
- **Memory**: Lower memory footprint (fewer dependencies)
- **Reliability**: Improved error handling and debugging
- **Maintainability**: Simpler codebase

This design maintains full backward compatibility while simplifying the architecture and improving performance.
