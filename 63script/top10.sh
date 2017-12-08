cat /home/log/cdn/access | awk '{print $9}' | sort | uniq -c | sort -rn | head
uptime
hostname
