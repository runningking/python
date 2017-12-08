#!/usr/bin/env bash

# @Time    : 2016/8/5 上午2:07
# @Author  : 吴彬
# @Site    : https://www.cnhzz.com
# @File    : hosts_ansible.sh
# @Software: vim
# @info    : 获取节点信息并接入 ansible 配置


# 清理 hosts 文件
echo >  ~/.ansible/hosts

# rtcp 版本
# python ~/.sbin/getnode --upnode && python ~/.sbin/getnode --upmd5

# mac 版
getnode --upnode && getnode --upmd5

# 定向输入分组变量配置到文件中去
{ 
    echo '[group_id:children]';seq 0 604;echo 'all-host' 
} | tee -a ~/.ansible/hosts

{
  echo '[group_id:vars]'
  echo 'ansible_ssh_port=22'
  echo 'ansible_ssh_user=log'
  echo 'ansible_ssh_private_key_file=~/.ssh/id_newxujing_rsa'
} | tee -a ~/.ansible/hosts

# 定向输入 hosts 分组信息
for i in `seq 0 604`
    do 
    {
        # echo [$i];python ~/.sbin/getnode -g $i | awk '{print $3}'
        echo ["$i"];getnode -g "$i" | awk '{print $3}'
    } | tee -a ~/.ansible/hosts
done
