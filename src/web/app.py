import sys
import os
import time
import threading
import json
from flask import Flask, render_template, jsonify
from flask_cors import CORS

# Add src to python path to import our modules
# Assuming this is running from project root or src/web
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from ingestion.log_reader import LogReader
from detection.engine import DetectionEngine
from detection.rules import BruteForceRule, PortScanRule, SuspiciousIPRule

app = Flask(__name__)
CORS(app)

# Configuration
LOG_FILE = os.path.abspath(os.path.join(src_dir, '..', 'data', 'logs', 'live_logs.json'))

# Global State
LATEST_LOGS = []
ALERTS = []
STATS = {
    "total_logs": 0,
    "total_alerts": 0,
    "brute_force_count": 0,
    "port_scan_count": 0,
    "suspicious_ip_count": 0
}

# Detection Setup
blacklist = ['192.168.1.100', '10.0.0.99', '185.100.100.100']
engine = DetectionEngine()
engine.add_rule(BruteForceRule(threshold=3))
engine.add_rule(PortScanRule())
engine.add_rule(SuspiciousIPRule(blacklist=blacklist))
reader = LogReader()

def background_process():
    """Reads logs periodically and runs detection."""
    global LATEST_LOGS, ALERTS, STATS
    print(f"[*] Background processor started. Watching {LOG_FILE}")
    
    last_processed_count = 0

    while True:
        try:
            if os.path.exists(LOG_FILE):
                # Read all logs (in a real app, we'd seek/tail)
                # Traffic generator limits file to 1000 lines, so reading all is fast enough
                logs = reader.read_logs(LOG_FILE)
                
                # Update Stats
                STATS["total_logs"] = len(logs)
                LATEST_LOGS = logs[-50:] # Keep last 50 for display
                LATEST_LOGS.reverse() # Newest first

                # Run detection on ALL logs for simplicity (stateless engine)
                # In a real system, we'd only run on new logs or use a window
                current_alerts = engine.run(logs)
                
                # Update Alerts
                ALERTS = current_alerts
                STATS["total_alerts"] = len(ALERTS)
                
                # Categorize alerts for stats
                bf = 0
                ps = 0
                sip = 0
                for a in ALERTS:
                    if "Brute Force" in a['rule']: bf += 1
                    elif "Port Scan" in a['rule']: ps += 1
                    elif "Suspicious IP" in a['rule']: sip += 1
                
                STATS["brute_force_count"] = bf
                STATS["port_scan_count"] = ps
                STATS["suspicious_ip_count"] = sip

        except Exception as e:
            print(f"[!] Error in background process: {e}")

        time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    return jsonify(STATS)

@app.route('/api/logs')
def get_logs():
    return jsonify(LATEST_LOGS)

@app.route('/api/alerts')
def get_alerts():
    # Return reversed to show newest first
    return jsonify(ALERTS[::-1])

if __name__ == '__main__':
    # Start background thread
    t = threading.Thread(target=background_process, daemon=True)
    t.start()
    
    print("[*] Starting Web Server on http://localhost:5000")
    app.run(debug=True, use_reloader=False) # use_reloader=False to prevent double threads
