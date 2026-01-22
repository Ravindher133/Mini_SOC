# Mini SOC Incident Monitoring & Alerting System

## 🚀 Overview
**Mini SOC** is a customized "junior SOC analyst" tool designed to simulate the core functions of a Security Operations Center. It monitors logs, detects suspicious activities (like brute force attacks, port scans, and malicious IPs), and generates real-time alerts.

This project demonstrates understanding of:
- **SIEM Concepts**: Log ingestion, normalization, and analysis.
- **Threat Detection**: Rule-based detection logic.
- **Incident Response**: Alert generation and triage.

## 📂 Project Structure
```
mini_soc/
├── data/
│   ├── logs/               # Sample CSV and JSON logs
│   └── threat_intel/       # (Expandable) Threat lists
├── src/
│   ├── ingestion/          # Modules for parsing CSV and JSON logs
│   ├── detection/          # Logic for detecting threats (Brute Force, etc.)
│   ├── alerting/           # Outputting alerts to console and file
│   └── main.py             # Main entry point for the application
├── tests/                  # Unit tests (Placeholder)
├── requirements.txt        # Project dependencies
└── alerts.log              # Log file where alerts are stored
```

## 🛡 Features
1.  **Multi-Format Log Ingestion**: Support for parsing `.csv` and `.json` log files.
2.  **Threat Detection Engine**:
    *   **Brute Force Detection**: Flags multiple failed login attempts from a single source.
    *   **Port Scan Detection**: Identifies patterns indicative of network scanning.
    *   **Suspicious IP Matching**: Cross-references source IPs against a threat intelligence blacklist.
3.  **Alerting System**:
    *   Color-coded console output for immediate visibility (Critical, High, Medium, Info).
    *   Persistent JSON-formatted logging to `alerts.log`.

## 🛠 Installation & Setup

### Prerequisites
*   Python 3.x installed.
*   (Optional) `pandas` if extending log ingestion capabilities.

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/Ravindher133/Mini_SOC.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd Mini_SOC/mini_soc
    ```
    *(Note: Ensure you are in the `mini_soc` inner folder where `src` exists)*

## 🚀 Usage

### 1. Run with Sample CSV Data
Run the tool against the provided CSV sample to see detection in action:
```bash
python src/main.py --input data/logs/sample.csv
```

### 2. Run with Sample JSON Data (Custom Threshold)
You can adjust detection thresholds (e.g., set brute force threshold to 1 for testing):
```bash
python src/main.py --input data/logs/sample.json --threshold 1
```

## 🧪 output Example
```text
[*] Reading logs from data/logs/sample.csv...
[*] Processed 5 log entries.
[*] Running detection engine...

[!] ALERT: 3 threats detected!

[HIGH] Brute Force Attempt - Source: 192.168.1.50
    Details: Detected 3 failed login attempts from 192.168.1.50
----------------------------------------
[MEDIUM] Port Scan Detected - Source: 192.168.1.100
    Details: Port scan activity detected from 192.168.1.100
----------------------------------------
[CRITICAL] Suspicious IP Activity - Source: 192.168.1.100
    Details: Activity detected from blacklisted IP: 192.168.1.100
----------------------------------------
```
