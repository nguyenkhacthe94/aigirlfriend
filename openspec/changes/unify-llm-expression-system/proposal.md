# Proposal: Unify LLM Expression System

## Summary

Refactor the current LLM mechanism to integrate vts_expressions functions through aisuite's function calling feature, creating a single unified system where the LLM both responds to users and expresses emotions simultaneously in one API call.

## Current State

The current system has several separated components:

- `llm_client.py` with emotion detection through JSON parsing
- `call_with_prompt_template` method for prompt management
- `llm_function_definitions.json` for complex function schemas
- Separate emotion prompts in `prompts/emotion_*.md`
- Manual emotion-to-expression mapping in main orchestration

## Proposed State

A unified system where:

- LLM receives user input and generates both text response AND expression in one call
- aisuite's function calling automatically handles vts_expressions functions
- Single system prompt guides both conversation and expression selection
- Removal of complex JSON schemas and template systems
- Direct integration between LLM decisions and VTS expressions

## Goals

1. **Simplify Architecture**: Remove multiple prompt templates, JSON schemas, and manual mapping
2. **Improve Responsiveness**: Single LLM call instead of multiple requests
3. **Better Integration**: Direct connection between conversational context and expressions
4. **Maintain Performance**: Keep <500ms response time requirement
5. **Reduce Complexity**: Eliminate custom prompt templating system

## Benefits

- **Single Point of Control**: One system prompt manages entire interaction
- **Natural Expression**: LLM directly chooses appropriate expressions based on conversation flow
- **Simplified Maintenance**: No JSON schema management or template updates
- **Better Coherence**: Expression choice informed by full conversational context
- **Performance Gain**: Eliminates second LLM call for emotion detection

## Risks and Mitigation

- **Risk**: aisuite function calling adds latency
  - **Mitigation**: Test with fast models (gpt-4o-mini, gemini-1.5-flash)
- **Risk**: LLM may not always call expression function
  - **Mitigation**: System prompt emphasizes expression requirement
- **Risk**: Complex debugging with function calls
  - **Mitigation**: Maintain existing expression debug scripts

## Implementation Scope

- Refactor `llm_client.py` to use aisuite function calling
- Create single unified system prompt
- Remove `call_with_prompt_template` and emotion prompt files
- Remove `llm_function_definitions.json`
- Update main orchestration to use new unified response
- Maintain compatibility with existing VTS connection system

## Success Criteria

1. Single `call_llm()` method returns both text response and expression
2. All vts_expressions functions available to LLM through aisuite
3. System maintains <500ms response time
4. Removal of prompt template system and emotion detection files
5. Expression choice quality matches or exceeds current system
