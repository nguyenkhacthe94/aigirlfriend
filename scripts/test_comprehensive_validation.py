#!/usr/bin/env python3
"""
Performance testing and validation for the unified LLM expression system.
Tests response time, expression quality, and system reliability.
"""

import asyncio
import os
import sys
import time
from typing import Dict, List

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import LLMClient


async def test_performance_requirements():
    """Test that the system meets <500ms response time requirements."""
    print("=== Performance Testing ===")

    try:
        client = LLMClient()
        print(f"Testing with: {client.provider}:{client.model}")

        # Test cases for performance
        test_inputs = [
            "Hi there!",
            "I'm so excited about this project!",
            "Can you help me understand something?",
            "That's frustrating.",
            "Wow, that's amazing!",
        ]

        response_times = []
        successful_calls = 0

        for i, test_input in enumerate(test_inputs, 1):
            print(f"\nTest {i}: '{test_input}'")

            try:
                start_time = time.time()
                response = client.call_llm(test_input)
                end_time = time.time()

                response_time_ms = (end_time - start_time) * 1000
                response_times.append(response_time_ms)
                successful_calls += 1

                print(f"  ✅ Response time: {response_time_ms:.0f}ms")
                print(f"  📝 Text: {response['text_response'][:50]}...")
                print(f"  😊 Expression: {response['expression_called'] or 'None'}")

                if response_time_ms > 500:
                    print(f"  ⚠️ Exceeds 500ms requirement")

            except Exception as e:
                print(f"  ❌ Failed: {e}")

        # Performance summary
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            under_500ms = sum(1 for t in response_times if t < 500)

            print(f"\n📊 Performance Summary:")
            print(f"  Successful calls: {successful_calls}/{len(test_inputs)}")
            print(f"  Average response time: {avg_time:.0f}ms")
            print(f"  Max response time: {max_time:.0f}ms")
            print(f"  Min response time: {min_time:.0f}ms")
            print(
                f"  Under 500ms: {under_500ms}/{len(response_times)} ({under_500ms/len(response_times)*100:.1f}%)"
            )

            # Pass criteria
            pass_rate = under_500ms / len(response_times) if response_times else 0
            if pass_rate >= 0.8:  # 80% of calls should be under 500ms
                print("  ✅ PASS: Meets performance requirements")
                return True
            else:
                print("  ❌ FAIL: Does not meet performance requirements")
                return False
        else:
            print("  ❌ No successful API calls")
            return False

    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False


async def test_expression_quality():
    """Test that expression selection quality is appropriate."""
    print("\n=== Expression Quality Testing ===")

    try:
        client = LLMClient()

        # Test cases with expected expression types
        quality_tests = [
            {
                "input": "Hello! How are you?",
                "expected_types": ["smile", "blink"],
                "should_avoid": ["angry", "sad", "love"],
            },
            {
                "input": "I'm so happy I got the job!",
                "expected_types": ["smile", "laugh", "wow"],
                "should_avoid": ["angry", "sad"],
            },
            {
                "input": "I'm feeling really upset about this.",
                "expected_types": ["sad", "blink"],
                "should_avoid": ["laugh", "smile", "love"],
            },
            {
                "input": "Yes, I completely agree with that!",
                "expected_types": ["agree", "smile"],
                "should_avoid": ["disagree", "angry"],
            },
            {
                "input": "What's the capital of France?",
                "expected_types": ["blink", None],  # Neutral question
                "should_avoid": ["love", "angry", "sad"],
            },
        ]

        quality_score = 0
        max_score = len(quality_tests)

        for i, test in enumerate(quality_tests, 1):
            print(f"\nQuality Test {i}: '{test['input']}'")

            try:
                response = client.call_llm(test["input"])
                expression = response["expression_called"]

                print(f"  Expression called: {expression or 'None'}")

                # Check if expression is appropriate
                is_appropriate = False
                if expression in test["expected_types"] or (
                    expression is None and None in test["expected_types"]
                ):
                    print("  ✅ Appropriate expression choice")
                    is_appropriate = True
                elif expression not in test["should_avoid"]:
                    print("  🤔 Acceptable expression choice")
                    is_appropriate = True
                else:
                    print(
                        f"  ❌ Poor expression choice (should avoid: {test['should_avoid']})"
                    )

                if is_appropriate:
                    quality_score += 1

            except Exception as e:
                print(f"  ❌ Test failed: {e}")

        print(
            f"\n📊 Quality Score: {quality_score}/{max_score} ({quality_score/max_score*100:.1f}%)"
        )

        if quality_score >= max_score * 0.7:  # 70% quality threshold
            print("  ✅ PASS: Expression quality is acceptable")
            return True
        else:
            print("  ❌ FAIL: Expression quality needs improvement")
            return False

    except Exception as e:
        print(f"❌ Quality test failed: {e}")
        return False


async def test_system_reliability():
    """Test system reliability with edge cases."""
    print("\n=== Reliability Testing ===")

    try:
        client = LLMClient()

        # Edge case tests
        edge_cases = [
            "",  # Empty input
            "   ",  # Whitespace only
            "a" * 1000,  # Very long input
            "🎉🎊😀",  # Emoji only
            "Hello\\nwith\\nnewlines",  # Multiline
            'Special chars: @#$%^&*()_+{}|:"<>?`~',
        ]

        reliability_score = 0

        for i, test_input in enumerate(edge_cases, 1):
            print(f"\nReliability Test {i}: {repr(test_input[:50])}")

            try:
                response = client.call_llm(test_input)

                # Check response structure
                if isinstance(response, dict) and "text_response" in response:
                    print("  ✅ Valid response structure")
                    reliability_score += 1
                else:
                    print("  ❌ Invalid response structure")

            except Exception as e:
                print(f"  ⚠️ Handled error: {e}")
                # Not necessarily a failure - some inputs should fail gracefully

        print(f"\n📊 Reliability Score: {reliability_score}/{len(edge_cases)}")

        # More lenient criteria for reliability
        if reliability_score >= len(edge_cases) * 0.5:
            print("  ✅ PASS: System handles edge cases reasonably")
            return True
        else:
            print("  ❌ FAIL: System reliability needs improvement")
            return False

    except Exception as e:
        print(f"❌ Reliability test failed: {e}")
        return False


async def run_comprehensive_validation():
    """Run all validation tests and provide final assessment."""
    print("🧪 Running Comprehensive Validation for Unified LLM Expression System")
    print("=" * 70)

    # Run all tests
    performance_pass = await test_performance_requirements()
    quality_pass = await test_expression_quality()
    reliability_pass = await test_system_reliability()

    # Final assessment
    print("\n" + "=" * 70)
    print("📋 FINAL ASSESSMENT")
    print("=" * 70)

    tests_passed = sum([performance_pass, quality_pass, reliability_pass])
    total_tests = 3

    print(f"Performance Test: {'✅ PASS' if performance_pass else '❌ FAIL'}")
    print(f"Expression Quality: {'✅ PASS' if quality_pass else '❌ FAIL'}")
    print(f"System Reliability: {'✅ PASS' if reliability_pass else '❌ FAIL'}")
    print(
        f"\nOverall Score: {tests_passed}/{total_tests} ({tests_passed/total_tests*100:.1f}%)"
    )

    if tests_passed == total_tests:
        print("\n🎉 SUCCESS: System is ready for production!")
        print("🚀 Ready for Task 7: Documentation and Scripts Update")
        return True
    elif tests_passed >= 2:
        print("\n⚠️ PARTIAL SUCCESS: System mostly works but has issues")
        print("🔧 Consider optimization before production use")
        return True
    else:
        print("\n❌ FAILURE: System needs significant work")
        print("🛠️ Address failing tests before proceeding")
        return False


if __name__ == "__main__":
    print("Note: This test requires a working LLM provider (Ollama, OpenAI, etc.)")
    print("If you don't have one configured, tests will fail - that's expected.\n")

    success = asyncio.run(run_comprehensive_validation())
    sys.exit(0 if success else 1)
