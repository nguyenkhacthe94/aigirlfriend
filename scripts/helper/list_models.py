#!/usr/bin/env python3
"""
Quick script to list available Google Generative AI models.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def load_env_file():
    """Load environment variables from .env file in project root."""
    env_path = project_root / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
        print(f"✅ Loaded environment variables from {env_path}")


def list_available_models():
    """List available models from Google Generative AI."""

    load_env_file()

    try:
        from google import genai

        # Initialize client
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not found")
            return

        client = genai.Client(api_key=api_key)

        # List models
        print("🔍 Available Google Generative AI models:")
        print("-" * 50)

        models = client.models.list()
        for model in models:
            print(f"📋 {model.name}")
            if hasattr(model, "supported_generation_methods"):
                print(f"   Supported methods: {model.supported_generation_methods}")
            print()

    except Exception as e:
        print(f"❌ Error listing models: {e}")


if __name__ == "__main__":
    list_available_models()
