#!/usr/bin/env python
"""
Simple test to verify authentication is working properly
"""

import subprocess
import time
import requests
import threading
import signal
import sys
import os

# Start the backend server in a separate thread
def start_backend():
    os.chdir('backend')
    proc = subprocess.Popen(['uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000'])
    return proc

def test_health_check():
    """Test that the backend is running and accessible"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f"Health check response: {response.status_code}, {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_protected_route():
    """Test that protected routes return 401 without auth"""
    try:
        # Try to access a protected route without authentication
        response = requests.get('http://localhost:8000/api/user123/tasks', timeout=5)
        print(f"Protected route response: {response.status_code}")
        # Should return 401 Unauthorized
        return response.status_code == 401
    except Exception as e:
        print(f"Protected route test failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting backend authentication test...")

    # Start backend server
    print("Starting backend server...")
    backend_proc = start_backend()

    # Give the server time to start
    time.sleep(3)

    try:
        # Test 1: Health check
        print("\n1. Testing health endpoint...")
        health_ok = test_health_check()
        print(f"Health check: {'PASS' if health_ok else 'FAIL'}")

        # Test 2: Protected route without auth
        print("\n2. Testing protected route without authentication...")
        protected_ok = test_protected_route()
        print(f"Protected route test: {'PASS' if protected_ok else 'FAIL'}")

        print(f"\nAuthentication system test: {'PASS' if health_ok and protected_ok else 'FAIL'}")

    finally:
        # Stop the backend server
        print("\nStopping backend server...")
        backend_proc.terminate()
        backend_proc.wait()
        print("Backend server stopped.")