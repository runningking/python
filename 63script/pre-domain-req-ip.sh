#zcat /home/log/cdn/access.$(date +%Y%m%d%H -d  '-1 hours').ncsa.gz | grep $1 | awk '{print $6}' | sort | uniq -c|sort -rn|head
zgrep v.pinpaibao.com /home/log/cdn/access.20170608*.ncsa.gz | awk '{print $6}' | sort | uniq -c | sort -rn | head
