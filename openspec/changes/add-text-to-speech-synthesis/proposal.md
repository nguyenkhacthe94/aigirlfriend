# Proposal: Add Text-to-Speech Synthesis

## Summary

Integrate Google's Gemini text-to-speech capabilities to generate audio files from AI responses, creating a synchronized audio-visual experience where the avatar speaks aloud while displaying expressions.

## Why

The current system provides an engaging visual experience with Live2D avatar expressions but lacks the audio dimension that would make interactions feel truly natural and immersive. Adding text-to-speech creates a complete AI girlfriend experience where users can both see and hear responses, significantly enhancing the emotional connection and realism of conversations. This positions the project as a comprehensive AI companion rather than a text-only chatbot with visual effects.

## Current State

The current system provides:

- Text responses from LLM via unified function calling
- Visual expressions through VTube Studio parameter injection 
- Real-time avatar animation based on detected emotions
- Audio folder exists but is unused in the main workflow

The user experience is currently visual-only with text responses displayed but no audio output.

## Proposed State

An enhanced system that:

- Generates audio files from LLM text responses using Google's Gemini TTS
- Saves audio files to the existing `audio/` directory with timestamp naming
- Provides synchronous TTS calls to maintain real-time experience
- Maintains the unified response system where text response, expression, and audio are coordinated

## Goals

1. **Audio-Visual Synchronization**: Generate speech that matches the avatar's expressions
2. **Minimal Latency**: Use synchronous calls to prevent blocking user interaction
3. **File Management**: Organized audio storage with automatic cleanup options
4. **Provider Integration**: Leverage existing google-genai client for TTS
5. **Simple Implementation**: Direct integration without complex audio streaming

## Benefits

- **Enhanced Immersion**: Full audio-visual AI girlfriend experience
- **Accessibility**: Audio output for users who prefer listening over reading
- **Natural Interaction**: Speaking avatar creates more realistic conversation
- **Unified Experience**: Single LLM call produces text, expression, and audio
- **File Preservation**: Audio responses saved for potential replay or analysis

## Risks and Mitigation

- **Risk**: TTS adds latency to response time
  - **Mitigation**: Use synchronous calls and fast Gemini TTS models
- **Risk**: Audio files consume disk space
  - **Mitigation**: Implement optional cleanup of old audio files
- **Risk**: TTS API costs increase usage expenses
  - **Mitigation**: Make TTS optional via configuration flag
- **Risk**: Audio generation failures break user experience
  - **Mitigation**: Graceful fallback to text-only responses

## Dependencies

- Existing google-genai client in llm_client.py
- Audio folder already present in project structure
- Google API key with TTS permissions
- Python wave module for audio file handling

## Success Criteria

- Audio files generated and saved for each AI response
- TTS integration doesn't exceed 500ms latency requirement
- Audio quality suitable for natural conversation
- System remains stable with fallback for TTS failures