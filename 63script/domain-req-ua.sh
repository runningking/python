cat /home/log/cdn/access | grep $1 | awk '{print $18}' | sort | uniq -c|sort -rn|head
