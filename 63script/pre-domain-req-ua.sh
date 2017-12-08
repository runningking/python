zcat /home/log/cdn/access.$(date +%Y%m%d%H -d  '-1 hours').ncsa.gz | grep $1 | awk '{print $18}' | sort | uniq -c|sort -rn|head
