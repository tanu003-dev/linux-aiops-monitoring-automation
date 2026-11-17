
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest

FILE = Path("linux_metrics.csv")
OUTPUT = Path("aiops_anomaly_results.csv")

columns = ["timestamp", "cpu", "memory", "disk", "processes"]
features = ["cpu", "memory", "disk", "processes"]

if not FILE.exists():
    print("Error: linux_metrics.csv not found.")
    raise SystemExit(1)

df = pd.read_csv(FILE, header=None, names=columns)

for column in features:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=features).copy()

if len(df) < 10:
    print("Please collect at least 10 valid readings first.")
    raise SystemExit(1)

# Machine learning: identify unusual patterns.
# "auto" avoids forcing a fixed 10% anomaly rate.
model = IsolationForest(
    contamination="auto",
    random_state=42
)

df["prediction"] = model.fit_predict(df[features])
df["anomaly_score"] = model.decision_function(df[features])

df["status"] = df["prediction"].map({
    1: "NORMAL",
    -1: "ANOMALY"
})

# Separate resource thresholds from ML anomaly detection.
# These thresholds are configurable starting points.
df["resource_status"] = (
    (df["cpu"] >= 80) |
    (df["memory"] >= 80) |
    (df["disk"] >= 80)
).map({
    True: "ALERT",
    False: "OK"
})

print("\n===== AIOps ML Anomaly Detection =====")
print(f"Total readings analyzed: {len(df)}")
print(f"Normal readings: {(df['status'] == 'NORMAL').sum()}")
print(f"Potential anomalies: {(df['status'] == 'ANOMALY').sum()}")
print(f"Resource threshold alerts: {(df['resource_status'] == 'ALERT').sum()}")

print("\nLatest 10 readings:")
display_columns = [
    "timestamp", *features, "status", "resource_status"
]
print(df[display_columns].tail(10).to_string(index=False))

df.to_csv(OUTPUT, index=False)

print(f"\nResults saved to {OUTPUT}")
print("ANOMALY means unusual pattern, not confirmed failure.")
print("ALERT means a configured resource threshold was reached.")
print("======================================")
