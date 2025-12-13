#!/usr/bin/env python3
"""
Configuration validation script for the abstract LLM client.
Helps users diagnose and fix configuration issues.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from llm_client import (
    DEFAULT_OLLAMA_URL,
    DEFAULT_PROVIDER,
    PROVIDER_MODEL_DEFAULTS,
    LLMClient,
)


def print_header(title):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print("=" * 60)


def print_check(description, status, details=""):
    """Print a configuration check result."""
    symbol = "✓" if status else "✗"
    print(f"{symbol} {description}")
    if details:
        print(f"  → {details}")


def check_environment_variables():
    """Check all environment variables."""
    print_header("Environment Variables")

    # Core variables
    provider = os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER)
    model = os.getenv("LLM_MODEL", "")
    timeout = os.getenv("LLM_TIMEOUT", "30")
    temp = os.getenv("LLM_TEMPERATURE", "0.0")

    print(f"LLM_PROVIDER: {provider} (default: {DEFAULT_PROVIDER})")

    default_model = PROVIDER_MODEL_DEFAULTS.get(provider, "unknown")
    model_display = model or f"(will use provider default: {default_model})"
    print(f"LLM_MODEL: {model_display}")
    print(f"LLM_TIMEOUT: {timeout} seconds")
    print(f"LLM_TEMPERATURE: {temp}")

    # Provider-specific variables
    print("\nProvider-specific configuration:")

    # Ollama
    ollama_url = os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL)
    print(f"OLLAMA_BASE_URL: {ollama_url}")

    # Google
    google_key = os.getenv("GOOGLE_API_KEY")
    print_check(
        "GOOGLE_API_KEY",
        bool(google_key),
        (
            "Set for Gemini access"
            if google_key
            else "Required for Google/Gemini provider"
        ),
    )

    # OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    print_check(
        "OPENAI_API_KEY",
        bool(openai_key),
        "Set for OpenAI access" if openai_key else "Required for OpenAI provider",
    )

    # Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    print_check(
        "ANTHROPIC_API_KEY",
        bool(anthropic_key),
        (
            "Set for Anthropic access"
            if anthropic_key
            else "Required for Anthropic provider"
        ),
    )


def check_providers():
    """Check provider availability."""
    print_header("Provider Status")

    providers = ["ollama", "google", "openai", "anthropic"]
    available_providers = []

    for provider in providers:
        try:
            # Try to create client to validate configuration
            client = LLMClient(provider=provider)
            print_check(
                f"{provider.capitalize()} Provider",
                True,
                "Ready to use",
            )
            available_providers.append(provider)
        except Exception as e:
            print_check(
                f"{provider.capitalize()} Provider",
                False,
                str(e),
            )

    print(
        f"\n{len(available_providers)} of {len(providers)} providers available: {', '.join(available_providers)}"
    )

    return available_providers


def check_current_configuration():
    """Check current configuration."""
    print_header("Current Configuration")

    provider = os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER)
    try:
        client = LLMClient()
        print_check(
            f"Selected Provider ({provider})",
            True,
            "Configuration valid",
        )
        print(f"✓ Model: {client.model}")
    except Exception as e:
        print_check(
            f"Selected Provider ({provider})",
            False,
            str(e),
        )
        print(f"✓ Ready for emotion detection")

    return is_valid


def provide_recommendations(available_providers, current_valid):
    """Provide configuration recommendations."""
    print_header("Recommendations")

    if current_valid:
        print("✅ Your current configuration is ready to use!")
        print("   No changes needed.")
    elif available_providers:
        print("💡 Configuration options:")
        for provider in available_providers:
            print(f"   • Use {provider}: export LLM_PROVIDER={provider}")
    else:
        print("⚠️  No providers are configured. Here's how to set them up:")
        print()
        print("🔧 Ollama (local, fastest):")
        print("   1. Install Ollama: https://ollama.ai/")
        print("   2. Run: ollama pull llama3")
        print("   3. Start Ollama server")
        print("   4. export LLM_PROVIDER=ollama")
        print()
        print("🔧 Google Gemini (cloud, balanced):")
        print("   1. Get API key: https://makersuite.google.com/app/apikey")
        print("   2. export GOOGLE_API_KEY=your_key_here")
        print("   3. export LLM_PROVIDER=google")
        print()
        print("🔧 OpenAI (cloud, popular):")
        print("   1. Get API key: https://platform.openai.com/api-keys")
        print("   2. export OPENAI_API_KEY=your_key_here")
        print("   3. export LLM_PROVIDER=openai")


def check_performance_considerations():
    """Check performance-related configuration."""
    print_header("Performance Considerations")

    provider = os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER)
    timeout = int(os.getenv("LLM_TIMEOUT", "30"))

    # Performance recommendations by provider
    perf_info = {
        "ollama": "Fastest (local), typically <200ms",
        "google": "Fast (cloud), typically <400ms with gemini-1.5-flash",
        "openai": "Moderate (cloud), may exceed 500ms with larger models",
        "anthropic": "Moderate (cloud), typically <500ms with claude-3-haiku",
    }

    print(f"Selected provider: {provider}")
    print(f"Expected performance: {perf_info.get(provider, 'Unknown')}")
    print(f"Timeout setting: {timeout}s")

    if timeout > 30:
        print("⚠️  High timeout may affect real-time performance")
    elif timeout < 10:
        print("⚠️  Low timeout may cause frequent failures")
    else:
        print("✓ Timeout setting looks good")

    # VTuber-specific guidance
    print("\n🎮 VTuber Performance Requirements:")
    print("   • Target: <500ms response time")
    print("   • Recommended: Use Ollama locally or Gemini Flash")
    print("   • Monitor: Response times will be logged")


def main():
    """Main validation function."""
    print("🔍 LLM Client Configuration Validator")

    check_environment_variables()
    available_providers = check_providers()
    current_valid = check_current_configuration()
    provide_recommendations(available_providers, current_valid)
    check_performance_considerations()

    print_header("Summary")

    if current_valid:
        print("🎉 Configuration is valid and ready to use!")
        print("   Run the main application or test scripts to continue.")
    else:
        print("❌ Configuration needs attention.")
        print("   Follow the recommendations above to fix issues.")
        exit(1)


if __name__ == "__main__":
    main()
