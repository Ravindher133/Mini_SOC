from typing import List, Dict, Any
import json
from datetime import datetime

class Alerter:
    def handle_alerts(self, alerts: List[Dict[str, Any]]):
        if not alerts:
            print("No threats detected.")
            return

        print(f"\n[!] ALERT: {len(alerts)} threats detected!\n")
        for alert in alerts:
            self._print_alert(alert)
            self._log_alert(alert)

    def _print_alert(self, alert: Dict[str, Any]):
        severity = alert.get('severity', 'INFO')
        rule = alert.get('rule', 'Unknown Rule')
        details = alert.get('details', 'No details provided.')
        source_ip = alert.get('source_ip', 'N/A')
        
        # Simple color coding using ANSI escape codes
        colors = {
            'CRITICAL': '\033[91m', # Red
            'HIGH': '\033[91m',     # Red
            'MEDIUM': '\033[93m',   # Yellow
            'LOW': '\033[94m',      # Blue
            'INFO': '\033[92m',     # Green
            'RESET': '\033[0m'
        }
        color = colors.get(severity, colors['RESET'])

        print(f"{color}[{severity}] {rule} - Source: {source_ip}{colors['RESET']}")
        print(f"    Details: {details}")
        print("-" * 40)

    def _log_alert(self, alert: Dict[str, Any]):
        # Append to alerts.log
        with open('alerts.log', 'a') as f:
            entry = {
                'timestamp': datetime.now().isoformat(),
                **alert
            }
            f.write(json.dumps(entry) + "\n")
