
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

scripts = [
    "analyze_metrics.py",
    "aiops_anomaly.py",
    "aiops_incidents.py",
    "aiops_decision.py",
    "aiops_ansible_bridge.py",
]

print("\n===== AIOps Master Pipeline =====")

for script in scripts:
    print(f"\n--- Running {script} ---")

    result = subprocess.run(
        [sys.executable, str(PROJECT_DIR / script)],
        cwd=PROJECT_DIR,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout, end="")

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        print(f"Pipeline stopped: {script} failed.")
        raise SystemExit(result.returncode)

print("\nAIOps pipeline completed successfully.")
print("No Ansible remediation was automatically executed.")
print("=================================")
