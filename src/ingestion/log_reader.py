import csv
import json
import os
from typing import List, Dict, Any

class LogReader:
    def __init__(self):
        pass

    def read_logs(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Reads logs from a file and returns a list of dictionaries.
        Supports CSV and JSON.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.csv':
            return self._read_csv(file_path)
        elif ext == '.json':
            return self._read_json(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    def _read_csv(self, file_path: str) -> List[Dict[str, Any]]:
        logs = []
        with open(file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)
        return logs

    def _read_json(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, 'r') as f:
            return json.load(f)

# Simple test if run directly
if __name__ == "__main__":
    reader = LogReader()
    # Assuming run from project root, adjust paths accordingly if direct execution
    # This is just for quick manual check if needed
    pass
