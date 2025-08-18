"""Quick helper to check if the backend API server is running."""
import requests
import sys
import os
import time

# Use environment variable or fallback to port 8080 (since 8000 is taken)
API_URL = os.environ.get("BACKEND_API_URL", "http://localhost:8080")

def check_server_health():
    """Try to connect to the server's /health endpoint."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Server is up! Response: {response.json()}")
            return True
        else:
            print(f"❌ Server returned error status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_until_responsive(timeout=30):
    """Check server health repeatedly until it responds or times out."""
    start_time = time.time()
    attempts = 0
    
    while time.time() - start_time < timeout:
        attempts += 1
        print(f"Attempt {attempts}: Checking if server is running...")
        if check_server_health():
            return True
        
        # Wait before trying again
        print(f"Waiting 2 seconds before retry...")
        time.sleep(2)
    
    print(f"❌ Server did not respond after {timeout} seconds")
    return False

if __name__ == "__main__":
    print("=" * 50)
    print("RAG Server Health Check")
    print("=" * 50)
    
    # See if server is running
    if check_server_health():
        sys.exit(0)
    
    print("\nTroubleshooting steps:")
    print("1. Make sure you've started the backend server with:")
    print("   powershell -ExecutionPolicy Bypass -File backend\\run_api.ps1")
    print("2. Check if there are any error messages in the backend terminal")
    print("3. Make sure port 8000 is not used by another application")
    print("4. Try restarting the backend server")
    print("=" * 50)
    
    # Wait mode if --wait flag is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--wait":
        print("Monitoring for server to become available...")
        if check_until_responsive(timeout=60):
            print("✅ Server is now responding!")
            sys.exit(0)
    
    sys.exit(1)
