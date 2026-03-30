import subprocess
import webbrowser
import time
import os

def start_portal():
    print("🚀 Initializing Event Portal...")
    
    # 1. Install dependencies (optional, assumes environment is ready)
    # subprocess.run(["pip", "install", "flask", "pymongo"])

    # 2. Start Flask App
    print("Starting Flask Backend...")
    # Using python directly to launch app.py
    process = subprocess.Popen(["python", "app.py"])

    # 3. Wait for boot and open browser
    time.sleep(2)
    print("Opening browser at http://localhost:5000...")
    webbrowser.open("http://localhost:5000")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        process.terminate()

if __name__ == "__main__":
    start_portal()
