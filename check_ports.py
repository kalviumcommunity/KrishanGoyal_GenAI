"""Port availability check script.

This script will check if port 8000 is available for the backend server.
"""
import socket

def is_port_in_use(port, host='localhost'):
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            # If connection succeeds, the port is in use
            s.connect((host, port))
            return True
        except (socket.error, socket.timeout):
            # Connection failed, port is available
            return False

if __name__ == "__main__":
    # Ports to check
    ports = [8000, 8501]
    
    print("=" * 60)
    print("PORT AVAILABILITY CHECK")
    print("=" * 60)
    
    for port in ports:
        if is_port_in_use(port):
            print(f"❌ Port {port} is ALREADY IN USE by another process!")
            print(f"   Try closing applications or changing the port.")
        else:
            print(f"✅ Port {port} is available.")
    
    print("\nIf ports are in use, you can find which process with:")
    print("netstat -ano | findstr :8000")
    print("netstat -ano | findstr :8501")
    print("=" * 60)
