#!/usr/bin/env python3
"""
Test script to verify system prompt loading and basic prompt structure.
"""

import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import LLMClient


def test_system_prompt():
    """Test that system prompt loads correctly."""
    print("Testing System Prompt Loading...")

    try:
        # Initialize LLM client
        client = LLMClient()

        # Load system prompt
        system_prompt = client._load_prompt("system")

        print(f"✅ System prompt loaded successfully!")
        print(f"   Length: {len(system_prompt)} characters")
        print(f"   First 100 chars: {system_prompt[:100]}...")

        # Check for key elements
        required_elements = [
            "VTuber AI Assistant",
            "expression functions",
            "helpful",
            "polite",
            "smile()",
            "laugh()",
            "Expression Rules",
        ]

        missing_elements = []
        for element in required_elements:
            if element not in system_prompt:
                missing_elements.append(element)

        if missing_elements:
            print(f"⚠️  Missing elements in prompt: {missing_elements}")
        else:
            print("✅ All required elements found in system prompt!")

        print("\n🎯 System prompt is ready for unified response system!")

    except Exception as e:
        print(f"❌ Error loading system prompt: {e}")
        return False

    return True


if __name__ == "__main__":
    test_system_prompt()
