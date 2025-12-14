#!/usr/bin/env python3
"""
Test script to verify vts_expressions function integration with aisuite.
This script tests basic function calling capability without full LLM integration.
"""

import asyncio
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


async def test_expression_functions():
    """Test that all expression functions can be imported and called."""
    print("Testing VTS Expression Functions for aisuite integration...")

    # List all expression functions
    expression_functions = [
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

    print(f"Found {len(expression_functions)} expression functions:")
    for func in expression_functions:
        print(
            f"  - {func.__name__}: {func.__doc__.split('.')[0] if func.__doc__ else 'No description'}"
        )

    # Test calling one function
    print("\nTesting function call:")
    await smile()

    # Test function signature inspection (what aisuite uses)
    print(f"\nFunction signature example for 'smile':")
    print(f"  Name: {smile.__name__}")
    print(
        f"  Docstring: {smile.__doc__[:100]}..." if smile.__doc__ else "  No docstring"
    )

    print("\n✅ All expression functions are ready for aisuite integration!")


if __name__ == "__main__":
    asyncio.run(test_expression_functions())
