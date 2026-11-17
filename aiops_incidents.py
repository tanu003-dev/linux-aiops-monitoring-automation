
import pandas as pd
from pathlib import Path
from datetime import datetime

INPUT_FILE = Path("aiops_anomaly_results.csv")
OUTPUT_FILE = Path("aiops_incident_report.csv")

if not INPUT_FILE.exists():
    print("Error: aiops_anomaly_results.csv not found.")
    raise SystemExit(1)

df = pd.read_csv(INPUT_FILE)
anomalies = df[df["status"] == "ANOMALY"].copy()

def classify_incident(row):
    reasons = []

    if row["cpu"] >= 80:
        reasons.append("High CPU")
    if row["memory"] >= 80:
        reasons.append("High Memory")
    if row["disk"] >= 80:
        reasons.append("High Disk Usage")

    if reasons:
        return ", ".join(reasons), "HIGH"

    # ML flagged the reading, but fixed thresholds look healthy.
    return "Unusual metrics pattern; investigate", "REVIEW"

if anomalies.empty:
    report = pd.DataFrame(columns=[
        "timestamp", "cpu", "memory", "disk",
        "processes", "status", "incident", "priority"
    ])
else:
    results = anomalies.apply(classify_incident, axis=1)
    anomalies[["incident", "priority"]] = pd.DataFrame(
        results.tolist(), index=anomalies.index
    )
    report = anomalies

report.to_csv(OUTPUT_FILE, index=False)

print("\n===== AIOps Incident Report =====")
print(f"Report generated: {datetime.now()}")
print(f"Potential incidents: {len(report)}")

if not report.empty:
    print(report[
        ["timestamp", "cpu", "memory", "disk",
         "incident", "priority"]
    ].to_string(index=False))
else:
    print("No potential anomalies found.")

print(f"\nSaved report to: {OUTPUT_FILE}")
print("=================================")
