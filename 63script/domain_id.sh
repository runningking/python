chgroup.py -g 556 --cn --list | grep -v 'CDN' | awk '{print $1}'
