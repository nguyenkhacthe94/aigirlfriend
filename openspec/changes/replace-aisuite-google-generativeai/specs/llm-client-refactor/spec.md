# LLM Client Refactor Specification

## MODIFIED Requirements

### Requirement: LLMClient Implementation

The LLMClient class SHALL be refactored to use google-generativeai directly instead of aisuite.

#### Scenario: Direct Google SDK Integration

GIVEN the project currently uses aisuite as an abstraction layer
WHEN the LLMClient is refactored  
THEN it SHALL use google-generativeai library directly
AND remove all aisuite dependencies
AND maintain identical public API interface

#### Scenario: Function Calling with Google Native SDK

GIVEN expression functions need to be called by the LLM
WHEN using google-generativeai directly
THEN function declarations SHALL be created using types.FunctionDeclaration.from_callable()
AND automatic function calling SHALL be enabled using Google's SDK features
AND response parsing SHALL maintain the same format as aisuite implementation

#### Scenario: Configuration Management

GIVEN the current configuration system uses environment variables
WHEN migrating to google-generativeai
THEN GOOGLE_API_KEY environment variable SHALL be required
AND LLM_MODEL SHALL default to "gemini-1.5-flash"
AND LLM_TEMPERATURE and LLM_TIMEOUT SHALL be preserved
AND provider-specific variables for non-Google providers SHALL be removed

#### Scenario: Response Format Compatibility

GIVEN main.py expects specific response format from LLMClient
WHEN the implementation changes to google-generativeai
THEN the response format SHALL remain unchanged
AND contain "text_response", "expression_called", and "intermediate_messages" fields
AND maintain backward compatibility for all consuming code

## REMOVED Requirements

### Requirement: Aisuite Dependency Management

The project SHALL no longer use aisuite for LLM provider abstraction.

#### Scenario: Aisuite Removal

GIVEN aisuite is currently used as the LLM provider abstraction
WHEN refactoring to google-generativeai
THEN aisuite dependency SHALL be removed from requirements.txt
AND all aisuite imports SHALL be removed from codebase
AND aisuite-specific configuration SHALL be removed

### Requirement: Multi-Provider Support

The LLMClient SHALL no longer support multiple LLM providers.

#### Scenario: Provider Limitation

GIVEN aisuite supported multiple providers (ollama, openai, anthropic, google)
WHEN migrating to google-generativeai only
THEN only Google/Gemini provider SHALL be supported
AND provider selection logic SHALL be simplified
AND non-Google provider configurations SHALL be removed

## ADDED Requirements

### Requirement: Google GenerativeAI Integration

The project SHALL integrate with google-generativeai SDK for LLM functionality.

#### Scenario: Google SDK Client Creation

GIVEN the need for LLM functionality
WHEN creating the LLMClient
THEN it SHALL use genai.Client() from google-generativeai
AND require GOOGLE_API_KEY for authentication
AND validate API key availability during initialization

#### Scenario: Native Function Declaration

GIVEN expression functions need schema definitions
WHEN setting up function calling
THEN types.FunctionDeclaration.from_callable() SHALL be used
AND automatic schema generation SHALL be enabled
AND function execution SHALL be handled by Google's SDK

#### Scenario: Performance Optimization

GIVEN the removal of aisuite abstraction layer
WHEN making LLM API calls
THEN direct API calls SHALL reduce latency
AND memory usage SHALL be optimized
AND fewer dependencies SHALL improve reliability

#### Scenario: Error Handling Enhancement

GIVEN google-generativeai provides specific error types
WHEN API errors occur
THEN Google-specific errors SHALL be caught and mapped
AND error messages SHALL be more descriptive
AND debugging information SHALL be improved
