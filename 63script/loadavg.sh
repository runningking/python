loadavg=`cat /proc/loadavg|cut -b 1-4`
full_loadavy=`cat /proc/loadavg`
processor=`cat /proc/cpuinfo|grep processor|wc -l`
xxxx=$(echo "scale=6;$loadavg/$processor"|bc)
hostname=`hostname`

echo "$xxxx $hostname $full_loadavy"
