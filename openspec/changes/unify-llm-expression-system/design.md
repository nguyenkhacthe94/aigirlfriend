# Design: Unified LLM Expression System

## Architecture Overview

This design creates a unified system where the LLM handles both conversational response and avatar expression selection in a single API call through aisuite's function calling capabilities.

### Current vs Proposed Architecture

#### Current Architecture

```
User Input → LLM (Emotion Detection) → JSON Parser → Emotion Mapping → VTS Expression
            ↓
            LLM (Response Generation) → Text Response
```

- 2 separate LLM calls
- Manual emotion→expression mapping
- Complex prompt templating system
- Separate JSON schema definitions

#### Proposed Architecture

```
User Input → LLM (Unified) → {Text Response + Expression Function Call}
                           ↓
                    aisuite Function Execution → VTS Expression
```

- Single LLM call with function calling
- Direct expression selection by LLM
- Unified system prompt
- aisuite handles function orchestration

## Technical Design

### 1. System Prompt Strategy

**Single Unified Prompt**: Combines conversational guidance with expression selection instructions.

**Key Elements**:

- Personality definition for the AI vTuber character
- Expression function descriptions (from vts_expressions docstrings)
- Rules for when to call expressions vs when to remain neutral
- Response style guidelines

**Design Principle**: The LLM should naturally choose appropriate expressions based on conversational context, not forced emotion detection.

### 2. Function Calling Integration

**aisuite Configuration**:

```python
# Tools array contains vts_expressions functions directly
tools = [smile, laugh, angry, blink, wow, agree, disagree, yap, shy, sad, love]

# Function calling with limited turns
response = client.chat.completions.create(
    model=model_string,
    messages=messages,
    tools=tools,
    max_turns=2  # Allow LLM to make one function call
)
```

**Function Selection Logic**:

- LLM analyzes user input and conversation context
- Chooses appropriate expression based on docstring guidance
- aisuite automatically executes the selected function
- No manual emotion detection or mapping required

### 3. Response Processing

**Unified Response Structure**:

```python
{
    "text_response": "LLM conversational response",
    "expression_called": "function_name" or None,
    "intermediate_messages": [...] # aisuite conversation history
}
```

**Processing Flow**:

1. LLM generates conversational response
2. LLM decides if expression is appropriate
3. aisuite executes expression function if called
4. Return combined result to main orchestration

### 4. Error Handling Strategy

**Function Call Failures**:

- If expression function fails, continue with text response
- Log expression errors for debugging
- Graceful degradation to text-only response

**Performance Fallbacks**:

- If response time >500ms, consider provider switching
- Monitor function call overhead through aisuite
- Implement basic timeout handling

## Implementation Considerations

### 1. Performance Optimization

**Response Time Targets**:

- Total response (text + expression): <500ms
- Function calling overhead: <50ms additional
- Provider-specific optimizations (faster models for real-time use)

**Optimization Strategies**:

- Use fast models: gpt-4o-mini, gemini-1.5-flash, claude-3-haiku
- Limit max_turns to minimize back-and-forth
- Cache system prompt to reduce token usage

### 2. Expression Quality Assurance

**LLM Expression Selection**:

- Rich docstrings in vts_expressions functions guide LLM choices
- System prompt emphasizes appropriate expression timing
- Context-aware selection (conversation flow, user emotional state)

**Quality Validation**:

- Compare expression selections to current emotion detection system
- A/B testing with different system prompt variations
- User feedback integration for expression appropriateness

### 3. Maintainability

**Code Simplification**:

- Remove prompt template infrastructure
- Eliminate JSON schema management
- Single source of truth for system behavior
- Simplified debugging (single LLM call path)

**Testing Strategy**:

- Manual testing remains primary approach (real-time interactivity)
- Simple test scripts for function calling verification
- Performance benchmarking for response times

## Migration Strategy

### Phase 1: Parallel Implementation

- Build new unified system alongside existing
- Maintain existing call paths during development
- Validate new system meets performance/quality requirements

### Phase 2: Switchover

- Update main orchestration to use new system
- Remove old emotion detection infrastructure
- Clean up deprecated files and methods

### Phase 3: Optimization

- Fine-tune system prompt based on usage patterns
- Optimize provider/model selection for best performance
- Enhance expression quality based on user feedback

## Risk Mitigation

### Technical Risks

**aisuite Function Calling Overhead**:

- **Risk**: Additional latency from function calling mechanism
- **Mitigation**: Benchmark against current system, optimize provider selection

**Expression Quality Regression**:

- **Risk**: LLM may make poor expression choices vs rule-based mapping
- **Mitigation**: Comprehensive testing, system prompt refinement

**Provider Compatibility Issues**:

- **Risk**: Function calling may not work consistently across providers
- **Mitigation**: Test with primary providers, fallback handling

### Operational Risks

**Debugging Complexity**:

- **Risk**: Function calling may be harder to debug than simple JSON parsing
- **Mitigation**: Maintain debug logging, create debugging scripts

**System Prompt Maintenance**:

- **Risk**: Single prompt becomes complex and hard to maintain
- **Mitigation**: Modular prompt design, clear documentation

## Success Metrics

### Performance Metrics

- Response time: <500ms (current requirement maintained)
- Function call success rate: >95%
- System availability: matches current system

### Quality Metrics

- Expression appropriateness: user feedback survey
- Conversational quality: maintained vs current system
- Expression variety: utilization of all available expressions

### Maintainability Metrics

- Code complexity: reduced LOC, fewer files
- Bug rate: tracking issues vs current implementation
- Development velocity: feature addition speed
