#!/usr/bin/env python3
"""
Windows Support Test Script for Skyvern

This script tests various Windows-specific functionality to ensure
Skyvern works correctly on Windows 11.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

def test_os_detection():
    """Test OS detection functionality."""
    print("🔍 Testing OS Detection...")
    
    system = platform.system()
    print(f"  Platform.system(): {system}")
    
    # Test detect_os function
    try:
        from skyvern.utils import detect_os
        detected_os = detect_os()
        print(f"  detect_os(): {detected_os}")
        
        if detected_os == "windows":
            print("  ✅ Windows detected correctly")
        else:
            print(f"  ⚠️  Expected 'windows', got '{detected_os}'")
            
    except ImportError as e:
        print(f"  ❌ Failed to import detect_os: {e}")
        return False
    
    return True

def test_chrome_path_detection():
    """Test Chrome path detection on Windows."""
    print("\n🌐 Testing Chrome Path Detection...")
    
    try:
        from skyvern.cli.browser import get_default_chrome_location
        from skyvern.utils import detect_os
        
        host_system = detect_os()
        chrome_path = get_default_chrome_location(host_system)
        print(f"  Detected Chrome path: {chrome_path}")
        
        if host_system == "windows":
            # Check if the path exists or is in a common Windows location
            if os.path.exists(chrome_path):
                print("  ✅ Chrome executable found")
            else:
                # Check common Windows Chrome locations
                common_paths = [
                    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                    os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"),
                ]
                
                found = False
                for path in common_paths:
                    if os.path.exists(path):
                        print(f"  ✅ Chrome found at: {path}")
                        found = True
                        break
                
                if not found:
                    print("  ⚠️  Chrome not found in common locations")
                    print("  💡 Please install Google Chrome or verify the installation")
        else:
            print(f"  ℹ️  Not testing on Windows (current OS: {host_system})")
            
    except ImportError as e:
        print(f"  ❌ Failed to import browser module: {e}")
        return False
    
    return True

def test_docker_commands():
    """Test Docker command execution on Windows."""
    print("\n🐳 Testing Docker Commands...")
    
    try:
        # Test basic Docker functionality
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            shell=True  # Use shell on Windows
        )
        
        if result.returncode == 0:
            print(f"  ✅ Docker version: {result.stdout.strip()}")
        else:
            print(f"  ❌ Docker not available: {result.stderr}")
            return False
            
        # Test Docker info
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("  ✅ Docker is running")
        else:
            print("  ⚠️  Docker is not running")
            print("  💡 Please start Docker Desktop")
            
    except Exception as e:
        print(f"  ❌ Docker test failed: {e}")
        return False
    
    return True

def test_python_environment():
    """Test Python environment and dependencies."""
    print("\n🐍 Testing Python Environment...")
    
    print(f"  Python version: {sys.version}")
    print(f"  Python executable: {sys.executable}")
    
    # Test required packages
    required_packages = [
        "typer",
        "rich",
        "playwright",
        "uvicorn",
        "fastapi",
        "psutil",
        "requests"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n  💡 Install missing packages: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_file_paths():
    """Test file path handling on Windows."""
    print("\n📁 Testing File Path Handling...")
    
    # Test path expansion
    home_dir = os.path.expanduser("~")
    print(f"  Home directory: {home_dir}")
    
    # Test Windows-specific paths
    if platform.system() == "Windows":
        appdata_local = os.path.expanduser("~\\AppData\\Local")
        appdata_roaming = os.path.expanduser("~\\AppData\\Roaming")
        
        print(f"  AppData\\Local: {appdata_local}")
        print(f"  AppData\\Roaming: {appdata_roaming}")
        
        if os.path.exists(appdata_local):
            print("  ✅ AppData\\Local exists")
        else:
            print("  ❌ AppData\\Local not found")
            
        if os.path.exists(appdata_roaming):
            print("  ✅ AppData\\Roaming exists")
        else:
            print("  ❌ AppData\\Roaming not found")
    
    return True

def test_skyvern_commands():
    """Test Skyvern CLI commands."""
    print("\n🚀 Testing Skyvern Commands...")
    
    try:
        # Test help command
        result = subprocess.run(
            ["skyvern", "--help"],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("  ✅ skyvern --help works")
        else:
            print(f"  ❌ skyvern --help failed: {result.stderr}")
            return False
            
        # Test status command
        result = subprocess.run(
            ["skyvern", "status"],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("  ✅ skyvern status works")
        else:
            print(f"  ⚠️  skyvern status failed: {result.stderr}")
            
    except Exception as e:
        print(f"  ❌ Skyvern command test failed: {e}")
        return False
    
    return True

def main():
    """Run all Windows support tests."""
    print("🧪 Skyvern Windows Support Test Suite")
    print("=" * 50)
    
    tests = [
        ("OS Detection", test_os_detection),
        ("Chrome Path Detection", test_chrome_path_detection),
        ("Docker Commands", test_docker_commands),
        ("Python Environment", test_python_environment),
        ("File Paths", test_file_paths),
        ("Skyvern Commands", test_skyvern_commands),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"  ❌ {test_name} failed")
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Skyvern should work well on Windows.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n💡 Common Windows Setup Steps:")
        print("1. Install Python 3.11+ from python.org")
        print("2. Install Docker Desktop from docker.com")
        print("3. Install Google Chrome")
        print("4. Run: pip install skyvern")
        print("5. Run: skyvern init")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 