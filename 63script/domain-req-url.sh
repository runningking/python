cat /home/log/cdn/access | grep $1 | awk '{print $10}' | sort | uniq -c | sort -rn | head
