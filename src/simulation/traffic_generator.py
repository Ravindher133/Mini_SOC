import json
import time
import random
import os
import datetime
from typing import List, Dict

# Configuration
LOG_FILE = os.path.join("data", "logs", "live_logs.json")
SLEEP_INTERVAL = 1.0  # Seconds between logs (approx)

# Mock Data
IPS = [
    "192.168.1.10", "192.168.1.11", "192.168.1.12", "192.168.1.20",  # Internal
    "10.0.0.5", "10.0.0.6", # More Internal
    "45.23.12.99", "185.100.100.100", "203.0.113.55" # External / Suspicious
]

USERS = ["admin", "alice", "bob", "service_account", "guest"]

STATUS_CODES = [200, 200, 200, 404, 401, 403, 500]

ENDPOINTS = ["/login", "/home", "/api/data", "/admin", "/contact", "/about"]

def get_timestamp():
    return datetime.datetime.now().isoformat()

def generate_normal_log():
    return {
        "timestamp": get_timestamp(),
        "ip": random.choice(IPS),
        "user": random.choice(USERS),
        "action": random.choice(["LOGIN_SUCCESS", "PAGE_VIEW", "API_CALL"]),
        "status": random.choice([200, 200, 200, 404]),
        "endpoint": random.choice(ENDPOINTS)
    }

def generate_brute_force_sequence(target_ip, target_user, attempts=5):
    logs = []
    for _ in range(attempts):
        logs.append({
            "timestamp": get_timestamp(),
            "ip": target_ip,
            "user": target_user,
            "action": "LOGIN_FAILED",
            "status": 401,
            "endpoint": "/login"
        })
        # Minimal delay to ensure unique timestamps if needed, or just same batch
        # timestamps in real files might be same second
    return logs

def generate_port_scan_sequence(target_ip):
    ports = [21, 22, 23, 80, 443, 3306, 8080]
    logs = []
    for port in ports:
        logs.append({
            "timestamp": get_timestamp(),
            "ip": target_ip,
            "user": "-",
            "action": "CONNECTION_ATTEMPT",
            "status": "REFUSED",
            "endpoint": f"port:{port}"
        })
    return logs

def ensure_file_exists():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)

def write_logs(new_logs: List[Dict]):
    # Read existing
    try:
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    # Append new
    data.extend(new_logs)
    
    # Keep file size manageable? Let's keep last 1000 for simplicity in this demo
    if len(data) > 1000:
        data = data[-1000:]

    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[*] Added {len(new_logs)} logs.")

def main():
    print(f"[*] Starting Traffic Generator. Writing to {LOG_FILE}...")
    ensure_file_exists()

    while True:
        choice = random.random()
        new_logs = []

        if choice < 0.1:
            # 10% chance of Brute Force
            attacker = "185.100.100.100" # Suspicious IP from blacklist
            print(f"[!] Simulating Brute Force from {attacker}")
            new_logs.extend(generate_brute_force_sequence(attacker, "admin"))
        elif choice < 0.15:
             # 5% chance of Port Scan
            attacker = "45.23.12.99"
            print(f"[!] Simulating Port Scan from {attacker}")
            new_logs.extend(generate_port_scan_sequence(attacker))
        else:
            # Normal traffic
            new_logs.append(generate_normal_log())

        write_logs(new_logs)
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    main()
