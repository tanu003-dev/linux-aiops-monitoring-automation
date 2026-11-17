#!/bin/bash

echo "================================="
echo "       SERVER HEALTH CHECK"
echo "================================="

echo ""
echo "Hostname:"
hostname

echo ""
echo "Date and Time:"
date

echo ""
echo "Uptime:"
uptime

echo ""
echo "Memory:"
free -h

echo ""
echo "Disk:"
df -h

# Check RAM usage
RAM_USAGE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')

echo ""
echo "RAM Usage: $RAM_USAGE%"

if [ "$RAM_USAGE" -ge 80 ]; then
    echo "WARNING: RAM usage is high!"
else
    echo "OK: RAM usage is normal."
fi

DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

echo ""
echo "Disk Usage: $DISK_USAGE%"

if [ "$DISK_USAGE" -ge 80 ]; then
    echo "WARNING: Disk usage is high!"
else
    echo "OK: Disk usage is normal."
fi

echo ""
echo "CPU Usage:"

CPU_USAGE=$(top -b -n 1 | awk '/Cpu\(s\)/ {print 100 - $8}')

printf "CPU Usage: %.1f%%\n" "$CPU_USAGE"

if (( $(echo "$CPU_USAGE >= 80" | bc -l) )); then
    echo "WARNING: CPU usage is high!"
else
    echo "OK: CPU usage is normal."
fi

echo ""
echo "CPU / PROCESSES:"
top -b -n 1 | head -15

echo ""
echo "================================="
echo "       CHECK COMPLETE"
echo "================================="
