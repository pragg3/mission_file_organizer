import os
import sys
import subprocess
import webbrowser
import time
import socket

def wait_for_server(host="127.0.0.1", port=8501, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

# Base path for script or exe
base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
os.chdir(base_path)

python_executable = sys.executable  # Use the portable Python

proc = subprocess.Popen([
    python_executable, "-m", "streamlit", "run", "app.py",
    "--server.port", "8501",
    "--server.address", "127.0.0.1",
    "--server.headless", "true",
    "--global.developmentMode", "false"
])

if wait_for_server():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8501")

proc.wait()
