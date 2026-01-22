from typing import List, Dict, Any
from .rules import DetectionRule

class DetectionEngine:
    def __init__(self):
        self.rules: List[DetectionRule] = []

    def add_rule(self, rule: DetectionRule):
        self.rules.append(rule)

    def run(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        all_alerts = []
        for rule in self.rules:
            alerts = rule.evaluate(logs)
            all_alerts.extend(alerts)
        return all_alerts
