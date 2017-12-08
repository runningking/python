cat /home/log/cdn/access | egrep "tengyin520.com|tengyin66.com"| grep -v 'MicroMessenger' |awk '{if($15==200)print $15,$10,$18}' | tail
