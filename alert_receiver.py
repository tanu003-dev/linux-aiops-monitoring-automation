from flask import Flask, request, jsonify
import subprocess
from datetime import datetime

app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def alert():
    data = request.json

    alerts = data.get("alerts", [])

    for alert in alerts:
        alert_name = alert.get("labels", {}).get("alertname", "Unknown")
        severity = alert.get("labels", {}).get("severity", "unknown")

        print(f"[{datetime.now()}] Alert received: {alert_name}")
        print(f"Severity: {severity}")

        if alert_name == "HighCPUUsage":
            print("Starting Ansible CPU remediation...")

            subprocess.Popen([
                "ansible-playbook",
                "-i",
                "ansible/inventory",
                "ansible/auto_remediation.yml"
            ])

    return jsonify({
        "status": "received",
        "alerts": len(alerts)
    })


@app.route("/")
def home():
    return "AIOps Alert Receiver is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
