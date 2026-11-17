import pandas as pd
from pathlib import Path

FILE = Path("linux_metrics.csv")

if not FILE.exists():
    print("Error: linux_metrics.csv not found.")
    raise SystemExit(1)

columns = ["timestamp", "cpu", "memory", "disk", "processes"]
df = pd.read_csv(FILE, header=None, names=columns)

if df.empty:
    print("Error: No metrics have been collected yet.")
    raise SystemExit(1)

print("\n========== AIOps Metrics Analysis ==========")

print(f"\nTotal readings: {len(df)}")

print("\nFirst 5 readings:")
print(df.head().to_string(index=False))

print("\nStatistical Summary:")
print(df[["cpu", "memory", "disk", "processes"]].describe().round(2))

print("\nCurrent Reading:")
print(df.iloc[-1][["timestamp", "cpu", "memory", "disk", "processes"]])

print("\n============================================")
