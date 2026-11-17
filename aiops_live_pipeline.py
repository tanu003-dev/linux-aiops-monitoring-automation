
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

import pandas as pd
import psutil

PROJECT = Path(__file__).resolve().parent
METRICS_FILE = PROJECT / "linux_metrics.csv"

def collect_reading():
    return {
        "timestamp": datetime.now().isoformat(sep=" "),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "processes": len(psutil.pids()),
    }

print("\n===== AIOps Live Pipeline =====")
print("Collecting 10 fresh readings...")

rows = []

for number in range(10):
    reading = collect_reading()
    rows.append(reading)

    print(
        f"{number + 1}/10 | "
        f"CPU: {reading['cpu']}% | "
        f"Memory: {reading['memory']}% | "
        f"Disk: {reading['disk']}% | "
        f"Processes: {reading['processes']}"
    )

    if number < 9:
        time.sleep(4)

# Append without a header to preserve the existing CSV format.
pd.DataFrame(rows).to_csv(
    METRICS_FILE,
    mode="a",
    header=False,
    index=False,
)

scripts = [
    "analyze_metrics.py",
    "aiops_anomaly.py",
    "aiops_incidents.py",
    "aiops_decision.py",
    "aiops_ansible_bridge.py",
]

for script in scripts:
    print(f"\n===== Running {script} =====")
    result = subprocess.run(
        [sys.executable, str(PROJECT / script)],
        cwd=PROJECT,
        text=True,
    )

    if result.returncode != 0:
        print(f"Pipeline stopped because {script} failed.")
        raise SystemExit(result.returncode)

print("\nLive AIOps pipeline completed.")
print("Anomaly flags are suggestions, not confirmed incidents.")
print("No Ansible remediation was automatically executed.")
