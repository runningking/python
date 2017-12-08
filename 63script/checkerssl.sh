#!/usr/bin/env bash
sshkey=id_newxujing_rsa

check_https(){
  tput bold
  tput setaf 2
  _domain=$1
  _ip_node=$2
  _http_code=$(echo | curl --resolve "$_domain":443:"$_ip_node" https://"$_domain" -o /dev/null -s -w %{http_code} | sed 's#%s##')
  _sdate=$(echo | openssl s_client -showcerts -servername "$_domain" -connect "$_ip_node":443 2>/dev/null |openssl x509 -noout -startdate |cut -d= -f2)
  _edate=$(echo | openssl s_client -showcerts -servername "$_domain" -connect "$_ip_node":443  2>/dev/null |openssl x509 -noout -enddate |cut -d= -f2)
  _issuer=$(echo | openssl s_client -showcerts -servername "$_domain" -connect "$_ip_node":443 2>/dev/null |openssl x509 -noout -issuer |sed 's/issuer=/颁发机构 : /')
  _dns=$(echo | openssl s_client -showcerts -servername "$_domain" -connect "$_ip_node":443 2>/dev/null | openssl x509 -noout -text | grep "DNS" | sed 's#DNS:##g' | sed 's/^[ \t]*//g')
  echo -e "域名:$_domain 访问节点:$_ip_node 网站访问状态码: $_http_code "
  echo -e "证书颁发时间: $_sdate 结束时间: $_edate. \n$_issuer"
  echo -e "证书绑定的域名:$_dns. "
  loadavg=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22 cat /proc/loadavg`
  processor=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22 cat /proc/cpuinfo| grep "processor"| wc -l`
  Mem=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22 free -g | grep "Mem" | awk '{print $2}'`
  ethspeed=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22 /sbin/ethtool eth0 2> /dev/null | grep  -i speed`
  xifstat=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22  bash < ~/.sbin/xifstat.sh 2> /dev/null`
  echo "负载情况："$loadavg
  echo "机器CPU核数"$processor "|" "机器内存:$Mem G"
  echo "网卡性能": $ethspeed "|" "实时流量":$xifstat
  tput sgr0

}

check_http(){
  tput bold
  tput setaf 2
  _ip_node=$2
  _domain=$1
  _http_code=$(echo | curl --resolve "$_domain":80:"$_ip_node" http://"$_domain" -o /dev/null -s -w %{http_code} | sed 's#%s##')
  echo -e "域名:$1 访问节点:$2 网站访问状态码: $_http_code "
  loadavg=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22 cat /proc/loadavg`
  processor=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22 cat /proc/cpuinfo| grep "processor"| wc -l`
  Mem=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22 free -g | grep "Mem" | awk '{print $2}'`
  ethspeed=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22 /sbin/ethtool eth0 2> /dev/null | grep  -i speed`
  xifstat=`ssh -i ~/.ssh/$sshkey -o StrictHostKeyChecking=no log@$2 -p 22  bash < ~/.sbin/xifstat.sh 2> /dev/null`
  echo "负载情况："$loadavg
  echo "机器CPU核数"$processor "|" "机器内存:$Mem G" 
  echo "网卡性能": $ethspeed "|" "实时流量":$xifstat
  tput sgr0
}

check_https_gid(){
  gid=$2
  domain=$1
  for ip in `getnode -g $gid | awk '{print $3}'`
  do
    check_https $domain $ip
    echo "========================================================================"
  done
}

check_http_gid(){
  gid=$2
  domain=$1
  for ip in `getnode -g $gid | awk '{print $3}'`
  do
    check_http $domain $ip
    echo "========================================================================"
  done
}

if [[ $1 == "ip" ]]; then
  if [[ $2 == "https" ]]; then
    check_https $3 $4
  elif [[ $2 == "http" ]]; then
    check_http $3 $4
  fi
elif [[ $1 == "gid" ]]; then
  if [[ $2 == "https" ]]; then
  check_https_gid $3 $4
  elif [[ $2 == "http" ]]; then
  check_http_gid $3 $4
  fi
else
  echo "
  查询分组: bash checkerssl.sh gid https www.yunaq.com 12
  查询IP：bash checkerssl.sh ip https www.yunaq.com 183.222.96.254
  "
fi

tput bold
tput setaf 2

tput sgr0

# check_http $1 $2
# check_https $1 $2
# check_http_gid $1 $2
# check_https_gid $1 $2
