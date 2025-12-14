# LLM Client Extension Capability

## MODIFIED Requirements

### Requirement: Response Object Structure

The LLMClient response object MUST be extended to include audio file information.

#### Scenario: Response with audio file path

**Given** a successful LLM response with TTS generation enabled
**When** the response is returned to the caller
**Then** the response MUST include an "audio_file" field
**AND** the field MUST contain the full path to the generated audio file
**AND** if TTS generation failed, the field MUST be None or empty string

#### Scenario: Response without TTS generation

**Given** TTS is disabled or unavailable
**When** generating an LLM response
**Then** the response MUST still include the "audio_file" field
**AND** the field value MUST be None
**AND** all other response fields MUST remain unchanged

### Requirement: Configuration Management

The LLMClient MUST support TTS-specific configuration through environment variables.

#### Scenario: TTS configuration loading

**Given** the LLMClient is initialized
**When** loading configuration settings
**Then** the system MUST read TTS_ENABLED environment variable (default: true)
**AND** read TTS_VOICE environment variable (default: "en-US-Casual")
**AND** read TTS_AUDIO_CLEANUP_DAYS environment variable (default: 7)
**AND** validate all TTS configuration values before use

#### Scenario: Invalid TTS configuration handling

**Given** TTS environment variables contain invalid values
**When** initializing the LLMClient
**Then** the system MUST fall back to default values for invalid settings
**AND** log warnings about invalid configuration
**AND** continue initialization successfully

## ADDED Requirements

### Requirement: TTS Method Integration

The LLMClient MUST provide a method to generate TTS audio from text responses.

#### Scenario: TTS generation method

**Given** a text response from the LLM
**When** the generate_tts_audio method is called
**Then** the method MUST accept text string and optional voice parameters
**AND** return the path to the generated audio file
**AND** handle all TTS API errors gracefully
**AND** use the existing google-genai client for TTS calls

#### Scenario: TTS method with custom parameters

**Given** specific voice or speed requirements
**When** calling generate_tts_audio with custom parameters
**Then** the method MUST override default settings for that call
**AND** preserve the default settings for future calls
**AND** validate custom parameters before TTS API calls

### Requirement: Error Handling Integration

TTS functionality MUST integrate with existing LLMClient error handling patterns.

#### Scenario: TTS error logging

**Given** a TTS generation failure occurs
**When** handling the error
**Then** the system MUST use existing logging patterns
**AND** categorize TTS errors as warnings, not failures
**AND** preserve the original text response functionality

#### Scenario: API key validation for TTS

**Given** TTS generation is requested
**When** validating API credentials
**Then** the system MUST verify the Google API key supports TTS operations
**AND** gracefully disable TTS if permissions are insufficient
**AND** continue with text-only responses if TTS is unavailable
