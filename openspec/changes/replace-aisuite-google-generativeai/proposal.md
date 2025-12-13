# Replace aisuite with google-generativeai Direct Usage

## Summary

Replace the current `aisuite` dependency with direct usage of `google-generativeai` library for better control, reduced dependencies, and improved reliability.

## Motivation

- **Simplify dependency chain**: Remove aisuite abstraction layer and use Google's native SDK directly
- **Better performance**: Eliminate overhead from aisuite wrapper
- **Enhanced functionality**: Access to latest Google-specific features not exposed through aisuite
- **Reduced maintenance**: Fewer dependencies to track and update
- **Better error handling**: More granular control over API interactions

## Current State

The project currently uses `aisuite` as a unified interface for multiple LLM providers, but only uses Google Gemini models. This abstraction layer adds complexity without benefits since we're locked to a single provider.

Current flow:

```
User Input → LLMClient (aisuite wrapper) → aisuite → google-generativeai → Gemini API
```

## Proposed Changes

### Dependencies

- **Remove**: `aisuite>=0.1.14`
- **Add**: `google-generativeai>=0.8.0`

### Core Implementation Changes

1. **llm_client.py Refactor**

   - Replace aisuite imports with google-generativeai
   - Implement function calling using Google's native SDK
   - Maintain same public API for backward compatibility
   - Keep existing configuration system (provider, model, temperature, etc.)

2. **Function Calling Migration**

   - Convert from aisuite's function calling to Google's native implementation
   - Use `google.genai.types.Tool` and `google.genai.types.FunctionDeclaration`
   - Implement automatic function calling using Google's SDK features
   - Maintain existing expression function integration

3. **Configuration Management**
   - Keep existing environment variable system
   - Maintain provider/model selection (limit to Google only)
   - Preserve timeout, temperature, and other parameters

### Benefits

1. **Performance**: Direct API calls without wrapper overhead
2. **Reliability**: Fewer dependencies and potential points of failure
3. **Features**: Access to latest Google-specific capabilities
4. **Maintenance**: Simpler codebase with fewer moving parts
5. **Debugging**: Clearer error traces and better diagnostics

## Impact Assessment

### Low Risk

- Same underlying API (google-generativeai)
- Maintaining identical public interface
- Comprehensive test coverage during migration

### Breaking Changes

- None for end users (same public API)
- Internal implementation details only

### Migration Strategy

1. Create new implementation alongside existing
2. Run comprehensive tests with both implementations
3. Switch implementation while preserving API
4. Remove aisuite dependencies
5. Update documentation

## Implementation Plan

1. **Phase 1**: Research and prototype google-generativeai direct usage
2. **Phase 2**: Implement new LLMClient with same API
3. **Phase 3**: Update tests and validate functionality
4. **Phase 4**: Update documentation and dependencies
5. **Phase 5**: Clean up and finalization
