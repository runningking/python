zcat /home/log/nlo/ngx/error.log.* | grep "2017/05/18" | grep dianrong.com | awk '$2 >="11:30:00" && $2 <="11:55:00"' | wc -l
hostname
