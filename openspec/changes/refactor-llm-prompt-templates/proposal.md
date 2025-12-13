# Change Proposal: Refactor LLM Client to Use Prompt Templates

## Summary

Refactor the LLM client to extract prompts into separate template files and standardize system/user prompt handling.

## Motivation

- **Maintainability**: Prompts scattered throughout code are hard to update and maintain
- **Consistency**: Standardize how system and user prompts are structured across the application
- **Flexibility**: Enable easy prompt customization without code changes
- **Best Practices**: Follow modern LLM application patterns with separated prompt management

## Changes

### 1. Remove Gemini Model Recommendation Logic

- Remove `get_gemini_model_recommendation()`, `configure_gemini()`, `is_gemini_configured()` functions
- Remove `GEMINI_MODELS` dictionary
- Simplify model selection to use only environment variables

### 2. Create Prompt Template System

- Create `prompts/` folder in project root
- Extract all prompts to `.md` files in prompts folder
- Add `_load_prompt()` method to LLMClient to read prompt files
- Add `call_with_prompt_template()` method to use template system

### 3. Standardize Message Structure

- Update `call_llm()` to accept separate system and user prompts
- Ensure consistent message structure across all providers
- Remove provider-specific prompt handling

### 4. Update Documentation

- Update AGENTS.md to guide putting all prompts in prompts/ folder
- Document new prompt template system
- Add examples of prompt template usage

## Implementation Tasks

1. ✅ Remove Gemini model recommendation functions
2. ✅ Create prompts/ folder and extract emotion detection prompts
3. ✅ Refactor LLMClient.call_llm() for system/user prompt structure
4. ✅ Add call_with_prompt_template() method
5. ✅ Update get_emotion_for_text() to use templates
6. ✅ Remove deprecated functions from test files
7. 🔄 Update openspec and AGENTS.md documentation
8. ⏳ Test refactored implementation

## Benefits

- Easier prompt engineering and iteration
- Cleaner separation of concerns
- Standardized LLM interaction patterns
- Better maintainability for prompt updates
