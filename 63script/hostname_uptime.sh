#! /bin/bash
_hostname=`cat /etc/hostname`
_uptime=`cat /proc/loadavg`
echo -n $_hostname $_uptime
