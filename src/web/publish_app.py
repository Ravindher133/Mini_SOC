import sys
import os
from pyngrok import ngrok
import threading

# Add src to path to allow importing app
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from web.app import app, background_process

def start_ngrok():
    # Helper to check for auth token if needed
    # ngrok.set_auth_token("YOUR_AUTHTOKEN")
    
    # Open a HTTP tunnel on the default port 5000
    public_url = ngrok.connect(5000).public_url
    print(f"\n[★] Public URL: {public_url}\n")
    print(f"[!] Access your Mini SOC Dashboard from anywhere using this link.")
    return public_url

if __name__ == "__main__":
    # Start the background detection thread (same as in app.py main)
    t = threading.Thread(target=background_process, daemon=True)
    t.start()

    # Start ngrok
    try:
        public_url = start_ngrok()
    except Exception as e:
        print(f"[X] Failed to start ngrok: {e}")
        print("[!] Assuming local run only.")

    print("[*] Starting Web Server...")
    # Run the app
    app.run(port=5000, use_reloader=False)
