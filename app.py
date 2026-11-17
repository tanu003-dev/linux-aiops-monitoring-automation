
from flask import Flask, jsonify
import psutil
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return "Linux Health Monitoring API is running"

@app.route('/health')
def health():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return jsonify({
        "hostname": socket.gethostname(),
        "status": "OK",
        "cpu_usage_percent": cpu,
        "ram_usage_percent": memory.percent,
        "ram_total_gb": round(memory.total / (1024**3), 2),
        "ram_used_gb": round(memory.used / (1024**3), 2),
        "disk_usage_percent": disk.percent,
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_used_gb": round(disk.used / (1024**3), 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
