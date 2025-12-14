#!/usr/bin/env python3
"""
Quick integration test for LLMClient with 3 test cases to avoid rate limiting.
"""

import os
import sys
import time
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


def test_quick_integration():
    """Test LLMClient with 3 different expressions to avoid rate limiting."""

    load_env_file()

    try:
        from llm_client import LLMClient
    except ImportError as e:
        print(f"❌ Error importing LLMClient: {e}")
        return False

    print("🧪 Quick Integration Test for LLMClient (3 tests)")
    print("=" * 50)

    try:
        client = LLMClient(provider="google", model="models/gemini-2.5-flash")
        print(f"✅ LLMClient initialized successfully")
        print(f"   Provider: {client.provider}")
        print(f"   Model: {client.model}")
    except Exception as e:
        print(f"❌ Failed to initialize LLMClient: {e}")
        return False

    # Limited test cases to avoid rate limiting
    test_cases = [
        {
            "input": "I'm so happy about this news!",
            "expected_emotions": ["smile", "laugh"],
        },
        {"input": "That's absolutely amazing!", "expected_emotions": ["wow", "smile"]},
        {"input": "Yes, I completely agree!", "expected_emotions": ["agree", "smile"]},
    ]

    print(f"\n🎯 Testing {len(test_cases)} different inputs...")
    print("-" * 50)

    results = []
    for i, test_case in enumerate(test_cases, 1):
        user_input = test_case["input"]
        expected_emotions = test_case["expected_emotions"]

        print(f"\nTest {i}: {user_input}")

        try:
            # Add delay to avoid rate limiting
            if i > 1:
                print("   ⏱️  Waiting 2 seconds to avoid rate limiting...")
                time.sleep(2)

            start_time = time.time()
            response = client.call_llm(user_input)
            call_time = time.time() - start_time

            text_response = response.get("text_response", "")
            expression_called = response.get("expression_called")

            has_text = bool(text_response.strip())
            has_expression = expression_called is not None
            expression_matches = (
                expression_called in expected_emotions if expression_called else False
            )

            print(
                f"   📝 Text Response: {text_response[:60]}{'...' if len(text_response) > 60 else ''}"
            )
            print(f"   🎭 Expression Called: {expression_called}")
            print(f"   ⏱️  Response Time: {call_time:.2f}s")
            print(f"   ✅ Has Text: {has_text}")
            print(f"   🎯 Has Expression: {has_expression}")

            if expression_called:
                match_status = "✅" if expression_matches else "⚠️"
                print(
                    f"   {match_status} Expression Match: {expression_matches} (expected: {expected_emotions})"
                )

            success = has_text and has_expression
            results.append(
                {"success": success, "expression": expression_called, "time": call_time}
            )

            if success:
                print(f"   🟢 PASS")
            else:
                print(f"   🔴 FAIL")

        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append({"success": False, "error": str(e)})

    # Summary
    print("\n" + "=" * 50)
    print("📊 QUICK TEST SUMMARY")
    print("=" * 50)

    successful = [r for r in results if r.get("success", False)]
    total = len(results)
    success_rate = len(successful) / total * 100

    print(f"Total Tests: {total}")
    print(f"Successful: {len(successful)}")
    print(f"Success Rate: {success_rate:.1f}%")

    if successful:
        avg_time = sum(r["time"] for r in successful) / len(successful)
        print(f"Average Response Time: {avg_time:.2f}s")

        expressions = [r["expression"] for r in successful if r.get("expression")]
        print(f"Expressions Called: {expressions}")

    if success_rate >= 66:  # At least 2 out of 3
        print("\n🎉 QUICK INTEGRATION TEST PASSED!")
        print("✅ LLMClient is working with google-generativeai")
        return True
    else:
        print("\n❌ QUICK INTEGRATION TEST FAILED!")
        return False


if __name__ == "__main__":
    success = test_quick_integration()
    sys.exit(0 if success else 1)
