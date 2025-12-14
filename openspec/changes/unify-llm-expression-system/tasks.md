# Implementation Tasks: Unify LLM Expression System

## Overview

Ordered tasks to refactor LLM mechanism for unified response and expression system using aisuite function calling.

## Tasks

### 1. Prepare Expression Function Integration - ✅ COMPLETED

**Description**: Set up vts_expressions functions for aisuite integration
**Duration**: 30 minutes
**Validation**: Import vts_expressions functions in llm_client.py without errors
**Dependencies**: None

**Subtasks**:

- ✅ Import all vts_expressions functions into llm_client.py
- ✅ Verify function docstrings are optimized for LLM understanding
- ✅ Test basic function calling with aisuite (using simple test script)

### 2. Create Unified System Prompt - ✅ COMPLETED

**Description**: Design single system prompt that guides both conversation and expression selection  
**Duration**: 45 minutes
**Validation**: New system prompt file created and tested
**Dependencies**: Task 1

**Subtasks**:

- ✅ Create `prompts/system.md` with unified instructions
- ✅ Include expression function guidance in system prompt
- ✅ Remove emotion-specific prompts (`emotion_system.md`, `emotion_user.md`)
- ✅ Test prompt clarity with sample inputs

### 3. Refactor LLMClient for Function Calling - ✅ COMPLETED

**Description**: Update llm_client.py to use aisuite function calling with vts_expressions
**Duration**: 60 minutes  
**Validation**: Single call_llm() method returns response and executes expression
**Dependencies**: Task 1, 2

**Subtasks**:

- ✅ Add vts_expressions functions as tools parameter in aisuite call
- ✅ Update call_llm() method to use function calling with max_turns=2
- ✅ Remove call_with_prompt_template() method
- ✅ Remove get_emotion_for_text() method
- ✅ Add response parsing for both text and expression execution

### 4. Update Main Orchestration

**Description**: Simplify main.py to use new unified LLM response system
**Duration**: 30 minutes
**Validation**: main.py works with single LLM call per user input  
**Dependencies**: Task 3

**Subtasks**:

### 4. Update Main Orchestration - ✅ COMPLETED

**Description**: Simplify main.py to use new unified LLM response system
**Duration**: 30 minutes  
**Validation**: main.py works with single LLM call per user input  
**Dependencies**: Task 3

**Subtasks**:

- ✅ Remove emotion mapping dictionaries
- ✅ Update main loop to use new unified call_llm() method
- ✅ Remove separate emotion detection calls
- ✅ Verify VTS integration still works correctly

### 5. Clean Up Deprecated Components - ✅ COMPLETED

**Description**: Remove no longer needed files and code
**Duration**: 20 minutes
**Validation**: Codebase cleaned of old emotion detection system
**Dependencies**: Task 4

**Subtasks**:

- ✅ Delete `llm_function_definitions.json`
- ✅ Delete emotion prompt files from `prompts/` folder
- ✅ Remove unused imports and helper methods
- ✅ Update any documentation references

### 6. Performance Testing and Validation - ✅ COMPLETED

**Description**: Verify system meets performance and quality requirements
**Duration**: 45 minutes
**Validation**: <500ms response time, expression quality maintained
**Dependencies**: Task 5

**Subtasks**:

- ✅ Test response time across different providers (ollama, openai, google)
- ✅ Verify expression selection quality with various inputs
- ✅ Test edge cases (no expression needed, multiple emotions)
- ✅ Create simple benchmark script for performance monitoring
- ✅ Validate all vts_expressions functions can be called correctly

### 7. Documentation and Scripts Update - ✅ COMPLETED

**Description**: Update documentation and test scripts for new system
**Duration**: 30 minutes
**Validation**: Documentation reflects new unified system
**Dependencies**: Task 6

**Subtasks**:

- ✅ Update AGENTS.md documentation
- ✅ Update scripts in `scripts/` folder for new system
- ✅ Create migration notes for users
- ✅ Test all debugging scripts work with new system

## Total Estimated Duration: 4 hours

## Parallel Work Opportunities

- Tasks 1 and 2 can be done in parallel
- Performance testing (Task 6) can begin once Task 3 is complete
- Documentation updates can happen alongside final testing

## Rollback Plan

If implementation fails or performance is unacceptable:

1. Revert llm_client.py changes
2. Restore prompt template files
3. Restore emotion detection methods
4. Test system returns to previous functionality

## Success Metrics - ✅ ALL ACHIEVED

- ✅ Single LLM call handles both response and expression
- ✅ Response time <500ms maintained (when LLM provider available)
- ✅ Expression quality matches current system
- ✅ Code complexity reduced (fewer files, methods)
- ✅ All existing VTS expressions still available

## IMPLEMENTATION STATUS: ✅ COMPLETED

All tasks have been successfully implemented. The unified LLM expression system is now fully functional with aisuite function calling integration.
