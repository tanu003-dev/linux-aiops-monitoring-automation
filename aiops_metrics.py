import psutil
import pandas as pd
import time
from datetime import datetime

FILE = "linux_metrics.csv"

print("Starting Linux metrics collection...")
print("Collecting metrics every 5 seconds.")
print("Press Ctrl+C to stop.")

while True:
    data = {
        "timestamp": datetime.now(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "processes": len(psutil.pids())
    }

    df = pd.DataFrame([data])

    try:
        df.to_csv(
            FILE,
            mode="a",
            header=False,
            index=False
        )
    except FileNotFoundError:
        df.to_csv(
            FILE,
            mode="w",
            header=True,
            index=False
        )

    print(
        f"{data['timestamp']} | "
        f"CPU: {data['cpu']}% | "
        f"Memory: {data['memory']}% | "
        f"Disk: {data['disk']}% | "
        f"Processes: {data['processes']}"
    )

    time.sleep(5)
