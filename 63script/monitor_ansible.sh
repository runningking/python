#! /bin/bash
loadavg_var=0.6
ansible "all-host" -f 101 -m script -a "/root/.sbin/loadavg.sh" | grep '"stdout": "'| sed -n 's/\"\./0./gp' | sed -n 's/\\r\\n",//gp' | awk '{if($2>='$loadavg_var') print $2,$3,$4,$5,$6}'
