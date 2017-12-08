ansible $1 -f 100 -m script -a "~/.sbin/top10.sh" | grep -A 13 stdout_lines
