import argparse
import sys
import os

# Add src to python path if running from root
sys.path.append(os.path.join(os.getcwd(), 'src'))

from ingestion.log_reader import LogReader
from detection.engine import DetectionEngine
from detection.rules import BruteForceRule, PortScanRule, SuspiciousIPRule
from alerting.alerter import Alerter

def main():
    parser = argparse.ArgumentParser(description="Mini SOC Incident Monitoring System")
    parser.add_argument('--input', '-i', required=True, help="Path to log file (CSV or JSON)")
    parser.add_argument('--threshold', '-t', type=int, default=3, help="Unsuccessful attempts threshold for Brute Force")
    
    args = parser.parse_args()

    # 1. Ingestion
    print(f"[*] Reading logs from {args.input}...")
    reader = LogReader()
    try:
        logs = reader.read_logs(args.input)
    except Exception as e:
        print(f"[X] Error reading logs: {e}")
        return

    print(f"[*] Processed {len(logs)} log entries.")

    # 2. Detection
    # Using some dummy blacklisted IPs for demonstration
    blacklist = ['192.168.1.100', '10.0.0.99', '185.100.100.100']
    
    engine = DetectionEngine()
    engine.add_rule(BruteForceRule(threshold=args.threshold))
    engine.add_rule(PortScanRule())
    engine.add_rule(SuspiciousIPRule(blacklist=blacklist))

    print("[*] Running detection engine...")
    alerts = engine.run(logs)

    # 3. Alerting
    alerter = Alerter()
    alerter.handle_alerts(alerts)

if __name__ == "__main__":
    main()
