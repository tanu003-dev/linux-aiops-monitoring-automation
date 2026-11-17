
import pandas as pd
from pathlib import Path
import subprocess

REPORT = Path("aiops_incident_report.csv")

if not REPORT.exists():
    print("Incident report not found. Run aiops_incidents.py first.")
    raise SystemExit(1)

df = pd.read_csv(REPORT)

print("\n===== AI-to-Ansible Safety Bridge =====")

if df.empty:
    print("No incidents found. No action required.")
else:
    high_count = 0
    review_count = 0

    for _, row in df.iterrows():
        print(f"\nTime: {row['timestamp']}")
        print(f"Incident: {row['incident']}")
        print(f"Priority: {row['priority']}")

        if row["priority"] == "HIGH":
            high_count += 1
            print("Action: HIGH priority. Manual approval required.")
            print("No playbook launched.")
        else:
            review_count += 1
            print("Action: Investigate. No playbook launched.")

    print(f"\nHIGH incidents: {high_count}")
    print(f"REVIEW incidents: {review_count}")

print("\nSafety: This bridge does not execute Ansible.")
print("=======================================")
