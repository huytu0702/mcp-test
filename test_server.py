#!/usr/bin/env python3
"""
Simple test script to verify the MCP server can be imported and initialized.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all imports work correctly."""
    try:
        import main

        print("✅ Successfully imported main module")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_mcp_initialization():
    """Test that the MCP server can be initialized."""
    try:
        from main import mcp

        print("✅ MCP server initialized successfully")
        print(f"   Server name: {mcp.name}")
        return True
    except Exception as e:
        print(f"❌ MCP initialization failed: {e}")
        return False


def test_api_connection():
    """Test API connection (without making actual requests)."""
    try:
        import requests

        print("✅ Requests library available")

        # Test API configuration
        from main import API_KEY, BASE_URL

        print(f"✅ API configuration loaded (key length: {len(API_KEY)})")
        print(f"   Base URL: {BASE_URL}")

        return True
    except Exception as e:
        print(f"❌ API configuration test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Testing Exchange Rates Data API MCP Server")
    print("=" * 50)

    tests = [
        ("Import Test", test_imports),
        ("MCP Initialization", test_mcp_initialization),
        ("API Configuration", test_api_connection),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1

    print("\n" + "=" * 50)
    print(f"✅ Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Server is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
