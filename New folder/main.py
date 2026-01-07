import webbrowser
import time
import threading
import sys
import os

# Add current directory to path so we can import server
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import server

def open_browser():
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open('http://localhost:8000')

def main():
    print("==========================================")
    print("   Hapi Mam Project - Premium File Carver")
    print("   Zero Dependencies | Pure Python")
    print("==========================================")
    print("[*] Starting server...")
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run server (blocking)
    try:
        server.run_server()
    except KeyboardInterrupt:
        print("\n[!] Stopping server...")
        sys.exit(0)

if __name__ == "__main__":
    main()
