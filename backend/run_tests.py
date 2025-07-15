#!/usr/bin/env python3
"""
Test runner script for the CRM API
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite"""
    print("🧪 Running CRM API Test Suite...")
    print("=" * 50)
    
    # Ensure we're in the parent directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run pytest with coverage on the backend package
    cmd = [
        sys.executable, "-m", "pytest",
        "backend/tests/",
        "--cov=backend",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with return code: {e.returncode}")
        return e.returncode

def run_specific_test(test_path):
    """Run a specific test file or test function"""
    print(f"🧪 Running specific test: {test_path}")
    print("=" * 50)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Ensure test path is relative to backend if not already
    if not test_path.startswith("backend/"):
        test_path = f"backend/{test_path}"
    
    cmd = [sys.executable, "-m", "pytest", test_path, "-v"]
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ Test {test_path} passed!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test {test_path} failed with return code: {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_path = sys.argv[1]
        sys.exit(run_specific_test(test_path))
    else:
        # Run all tests
        sys.exit(run_tests()) 