import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from ingestion.log_reader import LogReader

def test():
    reader = LogReader()
    csv_logs = reader.read_logs('data/logs/sample.csv')
    print(f"CSV Logs read: {len(csv_logs)}")
    print(csv_logs[0])

    json_logs = reader.read_logs('data/logs/sample.json')
    print(f"JSON Logs read: {len(json_logs)}")
    print(json_logs[0])

if __name__ == "__main__":
    test()
