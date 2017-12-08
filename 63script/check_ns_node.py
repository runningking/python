#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/6 下午2:01
# @Author  : wubin
# @Site    : https://www.cnhzz.com
# @File    : api.py
# @Software: PyCharm

import commands
import requests
import socket
import socks
import sys
from prettytable import PrettyTable

ns_node = [
    "113.207.76.90",
    "113.207.76.89",
    "113.207.76.7",
    "113.207.76.6",
    "117.21.219.80",
    "117.21.219.119",
    "117.21.219.120",
    "106.42.25.208",
    "106.42.25.141",
    "106.42.25.209",
    "180.97.158.160",
    "180.97.158.208",
    "180.97.158.110",
    "117.21.219.79",
    "117.21.219.118",
    "117.21.219.117",
    "111.202.98.111",
    "111.202.98.112",
    "119.188.35.26",
    "119.188.35.67",
    "119.188.35.68",
    "116.211.121.144",
    "116.211.121.142",
    "219.153.73.233",
    "116.211.121.145",
    "116.211.121.143",
"118.212.233.118",
"118.212.233.166",
"118.212.233.214",
"118.212.233.18",
"180.97.158.147",
"180.97.158.195",
"180.97.158.243",
]

#socks.set_default_proxy(socks.SOCKS5,addr='127.0.0.1',port=7070)
#socket.socket = socks.socksocket
x = PrettyTable(["NS主机名","NS节点IP", "解析出来的云安全IP", "绑定IP测试访问的状态码"])
x.padding_width = 1

for ns_ip in ns_node:
    cmd = "dig %s @%s +short" % (sys.argv[1],ns_ip)
    ns_hostname = commands.getstatusoutput("dig -x %s +short" % ns_ip)
    #print ns_hostname
    for node_ip in commands.getstatusoutput(cmd)[1].split():
        # print "NS节点:%s 解析出来的IP：%s" % (i, commands.getstatusoutput(cmd)[1].split())
        http_code = "curl -I --resolve %s:443:%s https://%s -o /dev/null -s -w %%{http_code}" % (sys.argv[1],node_ip,sys.argv[1])
        http_code_status = commands.getstatusoutput(http_code)
        # print ip,http_code_status[0]
        # node_ip_local = requests.get("http://freeapi.ipip.net/%s" % node_ip)
        # node_ip_info = "%s %s" % (node_ip_local.content,node_ip)

        x.add_row([ns_hostname[1],ns_ip, node_ip,http_code_status[1]])
        # print "NS节点:%s 解析出来的云安全IP：%s 访问状态码:%s" % (i, ip,http_code_status[1])
print x
