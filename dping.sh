#!/bin/bash

ping -c 1 $1 > /root/.sbin/ddos_domain.txt 2>&1
ip=`cat /root/.sbin/ddos_domain.txt|awk '{print $5}'|sed -n '2p'|awk -F '(' '{print $2}'|awk -F ')' '{print $1}'`
if [ ! -z ${ip} ] && [ ${ip} == $2 ]
then
	echo $1
fi
