from flask import Flask, jsonify, request
import platform
import psutil
import shutil
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return "Linux Health Monitoring API is running"


@app.route("/health")
def health():

    simulate_warning = request.args.get("simulate_warning", "false").lower() == "true"

    memory = psutil.virtual_memory()
    disk = shutil.disk_usage("/")

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = memory.percent
    disk_usage = round((disk.used / disk.total) * 100, 1)
    process_count = len(list(psutil.process_iter()))

    if simulate_warning:
        cpu_usage = 95.0
        status = "WARNING"
    elif cpu_usage >= 80 or memory_usage >= 80 or disk_usage >= 80:
        status = "WARNING"
    else:
        status = "OK"

    health_data = {
        "hostname": platform.node(),
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "processes": process_count,
        "status": status
    }

    return jsonify(health_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
