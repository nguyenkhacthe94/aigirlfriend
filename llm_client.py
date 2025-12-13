import json
import os
import sys
import time
from typing import Any, Dict, Optional

import aisuite as ai

from model_control.vts_expressions import (
    agree,
    angry,
    blink,
    disagree,
    laugh,
    love,
    sad,
    shy,
    smile,
    wow,
    yap,
)

# Configuration Constants
DEFAULT_PROVIDER = "ollama"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_TIMEOUT = 30
DEFAULT_TEMPERATURE = 0.75

# Expression functions for aisuite function calling
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
PROVIDER_MODEL_DEFAULTS = {
    "ollama": "llama3",
    "google": "gemini-1.5-flash",  # Fast model for real-time use
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-haiku",
}


class LLMClient:
    """Abstract LLM client providing unified interface for multiple AI providers."""

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """Initialize LLM client."""
        self._provider = provider or os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER).lower()
        self._model = model or os.getenv(
            "LLM_MODEL", PROVIDER_MODEL_DEFAULTS.get(self._provider, "llama3")
        )
        self._timeout = int(os.getenv("LLM_TIMEOUT", DEFAULT_TIMEOUT))
        self._temperature = float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE))

        # Provider-specific configuration
        self._ollama_base_url = os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL)
        self._google_api_key = os.getenv("GOOGLE_API_KEY")
        self._openai_api_key = os.getenv("OPENAI_API_KEY")
        self._anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        self._last_response_time: Optional[float] = None
        self._client: Optional[ai.Client] = None
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
        """Validate configuration and set up aisuite client."""
        if not self._validate_provider_config():
            raise ValueError(self._get_provider_validation_error())

        self._setup_provider_environment()
        self._client = self._create_client()

    def _validate_provider_config(self) -> bool:
        """Validate that the provider has all required configuration."""
        if self._provider == "ollama":
            return self._ollama_base_url.startswith("http")
        elif self._provider == "google":
            return bool(self._google_api_key)
        elif self._provider == "openai":
            return bool(self._openai_api_key)
        elif self._provider == "anthropic":
            return bool(self._anthropic_api_key)
        else:
            return False

    def _get_provider_validation_error(self) -> str:
        """Get descriptive error message for provider configuration issues."""
        if self._provider == "ollama":
            return f"Ollama provider configuration error. Set OLLAMA_BASE_URL environment variable (current: {self._ollama_base_url})"
        elif self._provider == "google":
            return "Google/Gemini provider requires GOOGLE_API_KEY environment variable. Get your API key from https://makersuite.google.com/app/apikey"
        elif self._provider == "openai":
            return "OpenAI provider requires OPENAI_API_KEY environment variable. Get your API key from https://platform.openai.com/api-keys"
        elif self._provider == "anthropic":
            return "Anthropic provider requires ANTHROPIC_API_KEY environment variable. Get your API key from https://console.anthropic.com/"
        else:
            return f"Unsupported provider: {self._provider}. Supported providers: ollama, google, openai, anthropic"

    def _setup_provider_environment(self) -> None:
        """Set up provider-specific environment variables."""
        if self._provider == "ollama" and self._ollama_base_url != DEFAULT_OLLAMA_URL:
            os.environ["OLLAMA_BASE_URL"] = self._ollama_base_url

    def _create_client(self) -> ai.Client:
        """Create and return configured aisuite client."""
        return ai.Client()

    def _get_model_string(self) -> str:
        """Get full model string for aisuite."""
        return f"{self._provider}:{self._model}"

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
            messages = []
            # load system prompt from prompt/ folder if not provided
            if not system_prompt:
                system_prompt = self._load_prompt("system")

            messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_prompt})

            response = self._client.chat.completions.create(
                model=self._get_model_string(),
                messages=messages,
                tools=EXPRESSION_TOOLS,  # Add expression functions as tools
                max_turns=2,  # Allow LLM to make one function call
                temperature=self._temperature,
                max_tokens=300,  # Increased for conversational responses
            )

            self._last_response_time = time.time() - start_time

            # Parse response for both text and expression
            return self._parse_unified_response(response)

        except Exception as e:
            self._last_response_time = time.time() - start_time
            raise Exception(f"LLM request failed: {e}")

    def _parse_unified_response(self, response) -> Dict[str, Any]:
        """Parse aisuite response for both text and expression function calls."""
        result = {
            "text_response": "",
            "expression_called": None,
            "intermediate_messages": [],
        }

        try:
            # Get the final response content
            final_message = response.choices[0].message
            result["text_response"] = final_message.content or ""

            # Get intermediate messages for function call analysis
            if hasattr(response.choices[0], "intermediate_messages"):
                result["intermediate_messages"] = response.choices[
                    0
                ].intermediate_messages

                # Look for function calls in intermediate messages
                for msg in result["intermediate_messages"]:
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        # Get the first function call (we limit to max_turns=2)
                        function_call = msg.tool_calls[0]
                        if (
                            hasattr(function_call, "function")
                            and function_call.function
                        ):
                            result["expression_called"] = function_call.function.name
                            break

        except Exception as e:
            print(f"Warning: Could not parse function calling response: {e}")
            # Fallback to basic text response
            result["text_response"] = (
                str(response.choices[0].message.content)
                if response.choices
                else "Error processing response"
            )

        return result

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
