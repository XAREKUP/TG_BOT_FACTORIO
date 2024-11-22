#!/bin/bash
disk=$(df -h . | tail -n 1)
disk_total=$(echo "$disk" | awk '{print $2}')
disk_used=$(echo "$disk" | awk '{print $3}')
disk_free=$(echo "$disk" | awk '{print $4}')

ram=$(free -m | grep Mem)
ram_total=$(echo "$ram" | awk '{print $2}')
ram_used=$(echo "$ram" | awk '{print $3}')
ram_free=$(echo "$ram" | awk '{print $4}')
cpu_idle=$(vmstat | tail -n 1 | awk '{print $15}')
cpu_usage=$(( 100 - $cpu_idle ))

echo "CPU usage: $cpu_usage%"
echo "RAM: total $ram_total MB, used $ram_used MB, free $ram_free MB"
echo "Disk: total $disk_total, used $disk_used, free $disk_free"

