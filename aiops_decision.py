
import pandas as pd
from pathlib import Path

FILE = Path("aiops_incident_report.csv")

if not FILE.exists():
    print("Incident report not found. Run aiops_incidents.py first.")
    raise SystemExit(1)

df = pd.read_csv(FILE)

print("\n===== AIOps Response Decision =====")

if df.empty:
    print("No incidents to review.")
else:
    for _, row in df.iterrows():
        print(f"\nTimestamp: {row['timestamp']}")
        print(f"Incident: {row['incident']}")
        print(f"Priority: {row['priority']}")

        if row["priority"] == "HIGH":
            print("Decision: Investigate and verify before remediation.")
        else:
            print("Decision: REVIEW required; no automatic changes.")

print("\nSafety: This script does not modify the system.")
print("===================================")
