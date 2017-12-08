for domain_id in `chgroup.py -g $1 --list | awk '{print $1}'`;do chgroup.py -i $domain_id -g $2;done
