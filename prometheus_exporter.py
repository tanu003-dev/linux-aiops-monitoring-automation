
from prometheus_client import start_http_server, Gauge
import psutil
import time
import socket
from pathlib import Path
import pandas as pd

# Existing Linux metrics
cpu_usage = Gauge("linux_cpu_usage_percent", "CPU usage percentage")
memory_usage = Gauge("linux_memory_usage_percent", "Memory usage percentage")
disk_usage = Gauge("linux_disk_usage_percent", "Disk usage percentage")
process_count = Gauge("linux_process_count", "Number of running processes")

# New AIOps metrics
ai_anomaly = Gauge(
    "aiops_anomaly_detected",
    "Latest reading flagged by the ML model: 1=yes, 0=no"
)
resource_alert = Gauge(
    "aiops_resource_threshold_alert",
    "Resource threshold alert: 1=alert, 0=normal"
)

hostname = socket.gethostname()
RESULTS_FILE = Path(__file__).resolve().parent / "aiops_anomaly_results.csv"

print(f"Starting Prometheus exporter for {hostname}...")
print("Metrics available on http://localhost:8000/metrics")

start_http_server(8000)

while True:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    processes = len(psutil.pids())

    cpu_usage.set(cpu)
    memory_usage.set(memory)
    disk_usage.set(disk)
    process_count.set(processes)

    # Resource thresholds are checked against live metrics.
    threshold_hit = cpu >= 80 or memory >= 80 or disk >= 80
    resource_alert.set(1 if threshold_hit else 0)

    # Read the most recent ML result, if available.
    # If the file is missing or unreadable, retain the last value.
    if RESULTS_FILE.exists():
        try:
            results = pd.read_csv(RESULTS_FILE)
            if not results.empty and "status" in results.columns:
                latest_status = str(results.iloc[-1]["status"])
                ai_anomaly.set(1 if latest_status == "ANOMALY" else 0)
        except (OSError, ValueError, pd.errors.ParserError) as error:
            print(f"Could not read AI results: {error}")

    time.sleep(5)
