import json
import os
import time
from typing import Any, Dict, Optional

import aisuite as ai

# Configuration Constants
DEFAULT_PROVIDER = "ollama"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_TIMEOUT = 30
DEFAULT_TEMPERATURE = 0.0  # For consistent JSON output

# Provider Model Defaults
PROVIDER_MODEL_DEFAULTS = {
    "ollama": "llama3",
    "google": "gemini-1.5-flash",  # Fast model for real-time use
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-haiku",
}


class LLMClient:
    """
    Abstract LLM client providing unified interface for multiple AI providers.

    This class encapsulates provider configuration, validation, and communication
    while maintaining backward compatibility with the existing emotion detection API.
    """

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM client with provider and model configuration.

        Args:
            provider: Provider name (ollama, google, openai, anthropic)
            model: Model name (provider-specific)
        """
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

        # Project root for prompt loading
        self._project_root = os.path.dirname(os.path.abspath(__file__))

        # Validate configuration on initialization
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

    def call_llm(self, user_prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Send prompts to the LLM and return the raw response.

        Args:
            user_prompt: The user message to send
            system_prompt: Optional system prompt (provider-specific behavior)

        Returns:
            str: Raw response from the LLM

        Raises:
            Exception: If the LLM request fails
        """
        if not self._client:
            raise RuntimeError("Client not initialized")

        start_time = time.time()
        try:
            # Build messages with proper system/user structure
            messages = []

            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # Add user prompt
            messages.append({"role": "user", "content": user_prompt})

            response = self._client.chat.completions.create(
                model=self._get_model_string(),
                messages=messages,
                temperature=self._temperature,
                max_tokens=150,  # Limit for JSON response
            )

            self._last_response_time = time.time() - start_time
            return response.choices[0].message.content

        except Exception as e:
            self._last_response_time = time.time() - start_time
            raise Exception(f"LLM request failed: {e}")

    def call_with_prompt_template(
        self, prompt_template_name: str, **template_vars
    ) -> str:
        """
        Call LLM using prompt templates from prompts/ folder.

        Args:
            prompt_template_name: Base name of prompt files (e.g. 'emotion' for emotion_system.md and emotion_user.md)
            **template_vars: Variables to substitute in user prompt template

        Returns:
            str: Raw response from the LLM
        """
        # Load system prompt
        system_prompt = self._load_prompt(f"{prompt_template_name}_system")

        # Load and format user prompt
        user_prompt_template = self._load_prompt(f"{prompt_template_name}_user")
        user_prompt = user_prompt_template.format(**template_vars)

        return self.call_llm(user_prompt, system_prompt)

    def get_emotion_for_text(self, text: str) -> dict:
        """
        Analyze text and return emotion classification using prompt templates.

        Args:
            text: Input text to analyze

        Returns:
            dict: {"emotion": "happy", "intensity": 0.8}
        """
        raw_response = self.call_with_prompt_template("emotion", text=text)
        return self._extract_json_from_text(raw_response)

    def _extract_json_from_text(self, raw: str) -> dict:
        """Extract JSON from LLM response."""
        try:
            start = raw.find("{")
            end = raw.rfind("}")
            if start == -1 or end == -1 or end < start:
                raise ValueError("No JSON object found")

            json_str = raw[start : end + 1]
            data = json.loads(json_str)

            # Validate and normalize
            emotion = data.get("emotion", "neutral")
            intensity = float(data.get("intensity", 0.5))
            intensity = max(0.0, min(1.0, intensity))

            return {"emotion": emotion, "intensity": intensity}

        except Exception as e:
            print(f"Warning: Could not parse LLM response as JSON: {e}")
            return {"emotion": "neutral", "intensity": 0.5}

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


# Global client instance for backward compatibility
_global_client: Optional[LLMClient] = None


def _get_global_client() -> LLMClient:
    """Get or create global LLM client instance."""
    global _global_client
    if _global_client is None:
        _global_client = LLMClient()
    return _global_client


def extract_json_from_text(raw: str) -> dict:
    """Extract JSON from LLM response (backward compatibility)."""
    return _get_global_client()._extract_json_from_text(raw)


def validate_provider_config(provider: Optional[str] = None) -> bool:
    """Validate provider configuration (backward compatibility)."""
    if provider:
        client = LLMClient(provider=provider)
        return client._validate_provider_config()
    return _get_global_client()._validate_provider_config()


def get_provider_validation_error(provider: Optional[str] = None) -> str:
    """Get provider validation error message (backward compatibility)."""
    if provider:
        client = LLMClient(provider=provider)
        return client._get_provider_validation_error()
    return _get_global_client()._get_provider_validation_error()


def get_model_string(
    provider: Optional[str] = None, model: Optional[str] = None
) -> str:
    """Get model string for provider (backward compatibility)."""
    if provider or model:
        client = LLMClient(provider=provider, model=model)
        return client._get_model_string()
    return _get_global_client()._get_model_string()


def call_llm(
    prompt: Optional[str] = None,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    user_prompt: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> str:
    """
    Send prompt to LLM (backward compatibility and new interface).

    Args:
        prompt: Legacy single prompt parameter (backward compatibility)
        provider: Optional provider override
        model: Optional model override
        user_prompt: New user prompt parameter (preferred)
        system_prompt: Optional system prompt parameter

    Returns:
        str: Raw response from the LLM

    Raises:
        ValueError: If both prompt and user_prompt are provided, or neither is provided
    """
    # Validate parameters
    if prompt and user_prompt:
        raise ValueError(
            "Cannot specify both 'prompt' and 'user_prompt'. Use 'user_prompt' for new code."
        )
    if not prompt and not user_prompt:
        raise ValueError(
            "Must specify either 'prompt' (legacy) or 'user_prompt' (preferred)."
        )

    # Create client
    if provider or model:
        client = LLMClient(provider=provider, model=model)
    else:
        client = _get_global_client()

    # Call with appropriate parameters
    if user_prompt:
        # New interface
        return client.call_llm(user_prompt, system_prompt)
    else:
        # Legacy interface - use prompt as user_prompt, no system prompt
        assert prompt is not None  # Already validated above
        return client.call_llm(prompt)


def get_emotion_for_text(text: str) -> dict:
    """Get emotion for text (backward compatibility)."""
    return _get_global_client().get_emotion_for_text(text)


def get_current_provider() -> str:
    """Get current provider name (backward compatibility)."""
    return _get_global_client().provider


def is_provider_available(provider: str) -> bool:
    """Check if provider is available (backward compatibility)."""
    try:
        client = LLMClient(provider=provider)
        return client._validate_provider_config()
    except Exception:
        return False


def validate_configuration() -> bool:
    """Validate current configuration (backward compatibility)."""
    try:
        client = _get_global_client()
        return True
    except ValueError:
        return False


def get_supported_providers() -> list[str]:
    """Get list of supported providers."""
    return list(PROVIDER_MODEL_DEFAULTS.keys())


def get_provider_models(provider: str) -> dict:
    """Get available models for a provider."""
    return {"default": PROVIDER_MODEL_DEFAULTS.get(provider, "unknown")}


# Test function
if __name__ == "__main__":
    sample_text = "Wow, that's amazing news!"
    try:
        # Validate configuration first
        if not validate_configuration():
            provider = os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER)
            print(f"Configuration error: {get_provider_validation_error(provider)}")
            exit(1)

        client = _get_global_client()
        print(f"Using provider: {client.provider}")
        print(f"Model: {client._get_model_string()}")

        result = get_emotion_for_text(sample_text)
        print("Input text:", sample_text)
        print("LLM emotion result:", result)
        print(f"Response time: {client.last_response_time:.3f}s")
        print(f"Performance OK: {client.is_performance_acceptable()}")

    except Exception as e:
        print(f"Error: {e}")
