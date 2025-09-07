#!/usr/bin/env python3
"""
Test runner script for Vexere AI Customer Service System
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests with coverage"""
    print("🧪 Running Vexere AI Customer Service Tests...")
    print("=" * 50)
    
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "app/tests/",
        "-v",
        "--tb=short",
        "--color=yes",
        "--durations=10"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return False

def run_specific_test(test_file):
    """Run specific test file"""
    print(f"🧪 Running {test_file}...")
    print("=" * 50)
    
    cmd = [
        sys.executable, "-m", "pytest",
        f"app/tests/{test_file}",
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ {test_file} tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {test_file} tests failed with exit code {e.returncode}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test file
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        # Run all tests
        success = run_tests()
    
    sys.exit(0 if success else 1)

