import json
import os
import sys
import time
from typing import Any, Dict, Optional

from google import genai
from google.genai import types

from model_control.vts_expressions import agree_sync as agree
from model_control.vts_expressions import angry_sync as angry
from model_control.vts_expressions import blink_sync as blink
from model_control.vts_expressions import disagree_sync as disagree
from model_control.vts_expressions import laugh_sync as laugh
from model_control.vts_expressions import love_sync as love
from model_control.vts_expressions import sad_sync as sad
from model_control.vts_expressions import shy_sync as shy
from model_control.vts_expressions import smile_sync as smile
from model_control.vts_expressions import wow_sync as wow
from model_control.vts_expressions import yap_sync as yap

# Configuration Constants
DEFAULT_PROVIDER = "google"
DEFAULT_TIMEOUT = 30
DEFAULT_TEMPERATURE = 0.75

# Expression functions for function calling
EXPRESSION_TOOLS = [
    smile,
    laugh,
    angry,
    blink,
    wow,
    agree,
    disagree,
    yap,
    shy,
    sad,
    love,
]

# Provider Model Defaults
PROVIDER_MODEL_DEFAULTS = "models/gemini-2.5-flash"


class LLMClient:
    """Abstract LLM client providing unified interface for multiple AI providers."""

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """Initialize LLM client."""
        self._provider = provider or os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER).lower()
        self._model = model or os.getenv(
            "LLM_MODEL",
            PROVIDER_MODEL_DEFAULTS,
        )
        self._timeout = int(os.getenv("LLM_TIMEOUT", DEFAULT_TIMEOUT))
        self._temperature = float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE))

        # Google API configuration
        self._google_api_key = os.getenv("GOOGLE_API_KEY")

        self._last_response_time: Optional[float] = None
        self._client: Optional[genai.Client] = None
        self._project_root = os.path.dirname(os.path.abspath(__file__))

        self._validate_and_setup()

    def _load_prompt(self, prompt_name: str) -> str:
        """Load prompt content from prompts/ folder."""
        prompt_path = os.path.join(self._project_root, "prompts", f"{prompt_name}.md")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    def _validate_and_setup(self) -> None:
        """Validate configuration and set up google-generativeai client."""
        if not self._validate_provider_config():
            raise ValueError(self._get_provider_validation_error())

        self._setup_provider_environment()
        self._client = self._create_client()

    def _validate_provider_config(self) -> bool:
        """Validate that the provider has all required configuration."""
        # Only support Google provider with google-generativeai
        if self._provider != "google":
            return False
        return bool(self._google_api_key)

    def _get_provider_validation_error(self) -> str:
        """Get descriptive error message for provider configuration issues."""
        if self._provider != "google":
            return f"Unsupported provider: {self._provider}. This version only supports 'google' provider."
        return "Google/Gemini provider requires GOOGLE_API_KEY environment variable. Get your API key from https://makersuite.google.com/app/apikey"

    def _setup_provider_environment(self) -> None:
        """Set up provider-specific environment variables."""
        # Set up Google API key if provided
        if self._google_api_key:
            os.environ["GOOGLE_API_KEY"] = self._google_api_key

    def _create_client(self) -> genai.Client:
        """Create and return configured google-generativeai client."""
        return genai.Client(api_key=self._google_api_key)

    def _get_model_string(self) -> str:
        """Get model string for google-generativeai."""
        return self._model

    def call_llm(
        self, user_prompt: str, system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send prompts to the LLM with function calling and return unified response.

        Returns:
            Dict containing:
            - text_response: The LLM's conversational response
            - expression_called: Name of expression function called (if any)
            - intermediate_messages: Full conversation history with function calls
        """
        if not self._client:
            raise RuntimeError("Client not initialized")

        start_time = time.time()
        try:
            # load system prompt from prompt/ folder if not provided
            if not system_prompt:
                system_prompt = self._load_prompt("system")

            # Combine system and user prompts
            combined_prompt = f"{system_prompt}\n\nUser: {user_prompt}"

            # First call to get potential function calls
            response = self._client.models.generate_content(
                model=self._get_model_string(),
                contents=combined_prompt,
                config=types.GenerateContentConfig(
                    tools=EXPRESSION_TOOLS,  # Add expression functions as tools
                    temperature=self._temperature,
                    max_output_tokens=300,  # Increased for conversational responses
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True  # Disable automatic calling so we can capture and execute manually
                    ),
                ),
            )

            self._last_response_time = time.time() - start_time

            # Check if there are function calls to process
            function_calls = []
            if hasattr(response, "function_calls") and response.function_calls:
                function_calls.extend(response.function_calls)
            elif hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if (
                    hasattr(candidate, "content")
                    and candidate.content
                    and hasattr(candidate.content, "parts")
                    and candidate.content.parts
                ):
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call"):
                            function_calls.append(part.function_call)

            # If we have function calls, execute them and continue conversation
            if function_calls:
                # Execute the first function call
                function_call = function_calls[0]
                function_name = None
                if hasattr(function_call, "name"):
                    function_name = function_call.name
                elif hasattr(function_call, "function_call") and hasattr(
                    function_call.function_call, "name"
                ):
                    function_name = function_call.function_call.name

                # Execute the function
                if function_name:
                    self._execute_function_call(function_call)

                # Create function response and continue conversation
                try:
                    if not function_name:
                        raise ValueError(
                            "Could not extract function name from function call"
                        )

                    function_response = types.Part.from_function_response(
                        name=function_name,
                        response={
                            "result": f"Expression {function_name} executed successfully"
                        },
                    )

                    # Continue conversation with function response
                    if not (hasattr(response, "candidates") and response.candidates):
                        raise ValueError("No candidates in response")

                    final_response = self._client.models.generate_content(
                        model=self._get_model_string(),
                        contents=[
                            types.Content(
                                role="user",
                                parts=[types.Part.from_text(text=combined_prompt)],
                            ),
                            response.candidates[0].content,  # The function call request
                            types.Content(
                                role="tool", parts=[function_response]
                            ),  # Our function response
                        ],
                        config=types.GenerateContentConfig(
                            tools=EXPRESSION_TOOLS,
                            temperature=self._temperature,
                            max_output_tokens=300,
                        ),
                    )

                    # Parse the final response
                    result = {
                        "text_response": final_response.text or "",
                        "expression_called": function_name,
                        "intermediate_messages": [
                            {
                                "role": "assistant",
                                "function_calls": [{"name": function_name, "args": {}}],
                            }
                        ],
                    }

                except Exception as e:
                    print(
                        f"Warning: Could not continue conversation after function call: {e}"
                    )
                    # Fallback to just the function call result
                    result = {
                        "text_response": f"*{function_name} expression*",  # Simple fallback
                        "expression_called": function_name,
                        "intermediate_messages": [],
                    }
            else:
                # No function calls, just return the text response
                result = {
                    "text_response": response.text or "",
                    "expression_called": None,
                    "intermediate_messages": [],
                }

            return result

        except Exception as e:
            self._last_response_time = time.time() - start_time
            raise Exception(f"LLM request failed: {e}")

    def _parse_unified_response(self, response) -> Dict[str, Any]:
        """Parse google-generativeai response for both text and expression function calls."""
        result = {
            "text_response": "",
            "expression_called": None,
            "intermediate_messages": [],
        }

        try:
            # Get text response
            result["text_response"] = response.text or ""

            # Check for function calls in multiple locations
            function_calls = []

            # Check response.function_calls (for automatic function calling)
            if hasattr(response, "function_calls") and response.function_calls:
                function_calls.extend(response.function_calls)

            # Check response.candidates[0].content.parts for function calls
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if (
                    hasattr(candidate, "content")
                    and candidate.content
                    and hasattr(candidate.content, "parts")
                    and candidate.content.parts
                ):
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call"):
                            function_calls.append(part.function_call)

            # Process function calls
            if function_calls:
                # Get the first function call
                function_call = function_calls[0]
                if hasattr(function_call, "name"):
                    result["expression_called"] = function_call.name
                elif hasattr(function_call, "function_call") and hasattr(
                    function_call.function_call, "name"
                ):
                    result["expression_called"] = function_call.function_call.name

                # Execute the function
                self._execute_function_call(function_call)

                # Store function calls info in intermediate messages
                result["intermediate_messages"] = [
                    {
                        "role": "assistant",
                        "function_calls": [
                            {
                                "name": getattr(
                                    fc,
                                    "name",
                                    getattr(fc, "function_call", {}).get(
                                        "name", "unknown"
                                    ),
                                ),
                                "args": getattr(
                                    fc,
                                    "args",
                                    getattr(fc, "function_call", {}).get("args", {}),
                                ),
                            }
                            for fc in function_calls
                        ],
                    }
                ]

        except Exception as e:
            print(f"Warning: Could not parse function calling response: {e}")
            # Fallback to basic text response
            result["text_response"] = (
                str(response.text)
                if hasattr(response, "text") and response.text
                else "Error processing response"
            )

        return result

    def _execute_function_call(self, function_call) -> None:
        """Execute the called function."""
        try:
            # Extract function name from different possible structures
            function_name = None
            if hasattr(function_call, "name"):
                function_name = function_call.name
            elif hasattr(function_call, "function_call") and hasattr(
                function_call.function_call, "name"
            ):
                function_name = function_call.function_call.name

            if not function_name:
                print(
                    f"Warning: Could not extract function name from function call: {function_call}"
                )
                return

            # Find and call the function from EXPRESSION_TOOLS
            for tool_func in EXPRESSION_TOOLS:
                if tool_func.__name__ == function_name:
                    # Execute the synchronous wrapper function directly
                    print(f"Executing expression function: {function_name}")
                    tool_func()
                    print(f"Successfully executed: {function_name}")
                    break
            else:
                print(
                    f"Warning: Function '{function_name}' not found in EXPRESSION_TOOLS"
                )
        except Exception as e:
            print(f"Warning: Could not execute function call: {e}")
            import traceback

            traceback.print_exc()

    @property
    def provider(self) -> str:
        """Get current provider name."""
        return self._provider

    @property
    def model(self) -> str:
        """Get current model name."""
        return self._model

    @property
    def last_response_time(self) -> Optional[float]:
        """Get last response time in seconds."""
        return self._last_response_time

    def is_performance_acceptable(self) -> bool:
        """Check if last response met performance requirements (<500ms)."""
        if self._last_response_time is None:
            return True
        return self._last_response_time < 0.5
