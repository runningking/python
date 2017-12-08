zcat /home/log/cdn/access.$(date +%Y%m%d%H -d  '-1 hours').ncsa.gz | awk '{print $9, $10}' | sort | uniq -c | sort -rn | head
