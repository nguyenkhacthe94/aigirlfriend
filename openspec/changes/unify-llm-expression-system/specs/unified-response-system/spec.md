# Unified Response System Specification

## ADDED Requirements

### Requirement: Single LLM Call Integration

The LLM client MUST handle both conversational response and expression selection in a single API call.

#### Scenario: User Greeting

**Given**: User sends "Hello! How are you today?"
**When**: LLM processes the input with function calling enabled
**Then**: System returns both text response ("Hello! I'm doing great, thanks for asking!") AND calls the `smile()` expression function
**And**: Total response time remains <500ms
**And**: No additional LLM calls are made for emotion detection

#### Scenario: Emotional User Input

**Given**: User sends "I just got a promotion at work!"
**When**: LLM processes the exciting news
**Then**: System returns congratulatory text response AND calls appropriate celebration expression (`laugh()` or `wow()`)
**And**: Expression choice reflects the excitement level appropriately

#### Scenario: Neutral Conversation

**Given**: User sends factual question "What's the weather like?"
**When**: LLM processes the neutral query
**Then**: System returns informative text response
**And**: May call `blink()` for natural animation or no expression at all
**And**: No inappropriate emotional expressions are triggered

### Requirement: aisuite Function Calling Integration

The system MUST use aisuite's function calling to directly invoke vts_expressions functions.

#### Scenario: Function Tool Registration

**Given**: LLM client is initialized
**When**: Function calling is configured
**Then**: All vts_expressions functions (smile, laugh, angry, blink, wow, agree, disagree, yap, shy, sad, love) are registered as available tools
**And**: Function docstrings are properly utilized by aisuite for LLM guidance

#### Scenario: Expression Function Execution

**Given**: LLM decides to call an expression function
**When**: aisuite executes the function call
**Then**: The corresponding expression function is invoked successfully
**And**: Function execution is tracked in intermediate_messages
**And**: Any function execution errors are handled gracefully without crashing

#### Scenario: Max Turns Limitation

**Given**: LLM call is configured with max_turns=2
**When**: LLM attempts multiple function calls
**Then**: System allows maximum of one expression function call per user input
**And**: Additional turns are prevented to maintain performance
**And**: Response is returned after expression function execution

### Requirement: Unified System Prompt

A single system prompt MUST guide both conversational behavior and expression selection.

#### Scenario: System Prompt Loading

**Given**: LLM client is initialized
**When**: System prompt is loaded from prompts/system.md
**Then**: Prompt includes personality definition for AI vTuber character
**And**: Prompt includes guidance for appropriate expression selection
**And**: Prompt replaces previous separate emotion detection prompts

#### Scenario: Expression Guidance Integration

**Given**: System prompt is active
**When**: LLM evaluates when to call expression functions
**Then**: LLM follows docstring guidance from vts_expressions functions
**And**: Expression selection is context-appropriate for conversation flow
**And**: LLM understands when NOT to call expression functions (neutral responses)

#### Scenario: Consistent Character Behavior

**Given**: Multiple user interactions with unified prompt
**When**: LLM responds across different conversation topics
**Then**: Character personality remains consistent across responses
**And**: Expression choices align with character personality
**And**: Conversational style matches defined vTuber persona

## REMOVED Requirements

### Requirement: Template-Based Prompt System

Remove the call_with_prompt_template method and associated template infrastructure.

#### Scenario: Template System Cleanup

**Given**: New unified system is implemented
**When**: Code refactoring is complete  
**Then**: `call_with_prompt_template` method is removed from LLMClient
**And**: Template variable substitution logic is eliminated
**And**: Template files in prompts/ folder are removed (emotion_system.md, emotion_user.md)

### Requirement: Separate Emotion Detection

Remove the dedicated emotion detection and JSON parsing system.

#### Scenario: Emotion Detection Removal

**Given**: Function calling system is active
**When**: Legacy emotion detection is removed
**Then**: `get_emotion_for_text` method is deleted from LLMClient
**And**: JSON emotion parsing logic is removed
**And**: Emotion intensity mapping is no longer used

#### Scenario: Function Definitions Cleanup

**Given**: aisuite handles function definitions automatically
**When**: Legacy function definition system is removed
**Then**: `llm_function_definitions.json` file is deleted
**And**: Manual JSON schema management is eliminated
**And**: Function definitions come directly from Python docstrings

## MODIFIED Requirements

### Requirement: LLMClient Interface

The LLMClient interface MUST be simplified to support unified response handling.

#### Scenario: Simplified Method Interface

**Given**: Refactored LLMClient class
**When**: `call_llm` method is invoked with user input
**Then**: Method accepts user_prompt and optional system_prompt parameters
**And**: Method returns structured response containing text and expression execution details
**And**: Method handles function calling internally without exposing complexity

#### Scenario: Response Structure Evolution

**Given**: New function calling integration
**When**: LLM response includes function calls
**Then**: Response object includes both text content and expression execution information
**And**: Intermediate messages from function calling are accessible for debugging
**And**: Response maintains backward compatibility for text-only usage

#### Scenario: Provider Configuration Maintenance

**Given**: Existing multi-provider support in LLMClient
**When**: Function calling is added
**Then**: All supported providers (ollama, openai, google, anthropic) maintain compatibility
**And**: Function calling works across different provider models
**And**: Provider-specific optimizations remain effective

### Requirement: Main Orchestration Simplification

The main application loop MUST be updated to use the new unified response system.

#### Scenario: Single Call Workflow

**Given**: New unified LLMClient interface
**When**: User input is processed in main.py
**Then**: Only one LLM call is made per user input
**And**: Both conversational response and expression are handled in this call
**And**: No separate emotion detection step is required

#### Scenario: Expression Mapping Elimination

**Given**: LLM directly selects expressions through function calling
**When**: Legacy emotion mapping dictionaries are removed
**Then**: `EMOTION_MAP` and similar mapping structures are deleted
**And**: Expression selection logic is handled entirely by LLM
**And**: Manual parameter injection for emotions is no longer needed

#### Scenario: VTS Integration Continuity

**Given**: Expression functions still interface with VTube Studio
**When**: Main orchestration is simplified
**Then**: VTS connection and authentication remain unchanged
**And**: Expression function calls still trigger VTS parameter updates
**And**: Overall VTS integration performance is maintained
