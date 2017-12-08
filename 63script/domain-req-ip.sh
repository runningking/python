cat /home/log/cdn/access | grep $1 | awk '{print $6}' | sort | uniq -c | sort -rn | head
