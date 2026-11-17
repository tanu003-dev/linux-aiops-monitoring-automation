#!/usr/bin/env python3

import os
import json
import platform
import shutil
import psutil
from datetime import datetime


print("=================================")
print("       SERVER HEALTH CHECK")
print("=================================")

# Hostname
print("\nHostname:")
print(platform.node())

# Date and time
print("\nDate and Time:")
print(datetime.now())

# Uptime
print("\nUptime:")
with open("/proc/uptime", "r") as file:
    uptime_seconds = float(file.readline().split()[0])

hours = int(uptime_seconds // 3600)
minutes = int((uptime_seconds % 3600) // 60)

print(f"{hours} hours {minutes} minutes")

# Memory
print("\nMemory:")

with open("/proc/meminfo", "r") as file:
    memory = file.readlines()

total_memory = 0
available_memory = 0

for line in memory:
    if line.startswith("MemTotal:"):
        total_memory = int(line.split()[1])
    elif line.startswith("MemAvailable:"):
        available_memory = int(line.split()[1])

used_memory = total_memory - available_memory
memory_usage = (used_memory / total_memory) * 100

print(f"Total Memory: {total_memory / 1024 / 1024:.2f} GB")
print(f"Used Memory: {used_memory / 1024 / 1024:.2f} GB")
print(f"Memory Usage: {memory_usage:.1f}%")

if memory_usage >= 80:
    print("WARNING: Memory usage is high!")
else:
    print("OK: Memory usage is normal.")

# Disk
print("\nDisk:")

disk = shutil.disk_usage("/")

disk_total = disk.total
disk_used = disk.used
disk_free = disk.free

disk_usage = (disk_used / disk_total) * 100

print(f"Total Disk: {disk_total / 1024**3:.2f} GB")
print(f"Used Disk: {disk_used / 1024**3:.2f} GB")
print(f"Free Disk: {disk_free / 1024**3:.2f} GB")
print(f"Disk Usage: {disk_usage:.1f}%")

if disk_usage >= 80:
    print("WARNING: Disk usage is high!")
else:
    print("OK: Disk usage is normal.")

# CPU
print("\nCPU:")

cpu_usage = psutil.cpu_percent(interval=1)

print(f"CPU Usage: {cpu_usage:.1f}%")

if cpu_usage >= 80:
    print("WARNING: CPU usage is high!")
else:
    print("OK: CPU usage is normal.")

# Processes
print("\nProcesses:")

process_count = len(list(psutil.process_iter()))

print(f"Running Processes: {process_count}")

# Create JSON data
health_data = {
    "hostname": platform.node(),
    "cpu_usage": round(cpu_usage, 1),
    "memory_usage": round(memory_usage, 1),
    "disk_usage": round(disk_usage, 1),
    "processes": process_count
}

# Display JSON
print("\nJSON HEALTH DATA:")
print(json.dumps(health_data, indent=4))

# Save JSON to a file
with open("health_report.json", "w") as file:
    json.dump(health_data, file, indent=4)

print("\nJSON report saved to health_report.json")

print("\n=================================")
print("       CHECK COMPLETE")
print("=================================")
