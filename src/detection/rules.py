from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DetectionRule(ABC):
    @abstractmethod
    def evaluate(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Evaluates the logs and returns a list of alerts.
        """
        pass

class BruteForceRule(DetectionRule):
    def __init__(self, threshold: int = 3):
        self.threshold = threshold

    def evaluate(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alerts = []
        failed_attempts = {}

        for log in logs:
            if log.get('event_type') == 'login' and log.get('status') == 'failed':
                src_ip = log.get('source_ip')
                if src_ip not in failed_attempts:
                    failed_attempts[src_ip] = 0
                failed_attempts[src_ip] += 1

        for ip, count in failed_attempts.items():
            if count >= self.threshold:
                alerts.append({
                    'rule': 'Brute Force Attempt',
                    'severity': 'HIGH',
                    'source_ip': ip,
                    'details': f"Detected {count} failed login attempts from {ip}"
                })
        return alerts

class PortScanRule(DetectionRule):
    def evaluate(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alerts = []
        # Simple rule: if event_type explicitly says 'port_scan'
        # Or, could count unique destination ports. 
        # Given sample data, we'll check for 'port_scan' event type.
        for log in logs:
            if log.get('event_type') == 'port_scan':
                alerts.append({
                    'rule': 'Port Scan Detected',
                    'severity': 'MEDIUM',
                    'source_ip': log.get('source_ip'),
                    'details': f"Port scan activity detected from {log.get('source_ip')}"
                })
        return alerts

class SuspiciousIPRule(DetectionRule):
    def __init__(self, blacklist: List[str]):
        self.blacklist = set(blacklist)

    def evaluate(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alerts = []
        for log in logs:
            if log.get('source_ip') in self.blacklist:
                alerts.append({
                    'rule': 'Suspicious IP Activity',
                    'severity': 'CRITICAL',
                    'source_ip': log.get('source_ip'),
                    'details': f"Activity detected from blacklisted IP: {log.get('source_ip')}"
                })
        return alerts
