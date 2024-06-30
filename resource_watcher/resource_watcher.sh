#!/bin/sh


while true; do
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '$8 != "id," {printf("%.0f\n", 100 - $8)}')

if [ -z "$cpu_usage" ]; then
        cpu_usage=0
fi


if [ $cpu_usage -gt "80" ]; then
        python3 discord_hook.py cpu $cpu_usage
fi

mem_usage=$(free | grep Mem | awk '{printf("%.0f\n", $3 / $2 * 100)}')

if [ $mem_usage -gt "80" ]; then
        python3 discord_hook.py mem $mem_usage
fi

sleep 1

done