#! /bin/bash
old_hosts_ansible.sh && echo "[all-host]" | tee -a ~/.ansible/hosts ;for i in `cat /var/tmp/lan.txt`;do getnode -l $i|awk '{print $3}'|grep -v '^$' | grep -v "None"|grep -v "^203.90"|grep -v "^112.25"|grep -v "^111.202"|grep -v "^58.215"|grep -v "123.155.158.62"|grep -v "60.191.97.109"|grep -v "^222.240";done | tee -a ~/.ansible/hosts && get_idc_wip | tee -a ~/.ansible/hosts
