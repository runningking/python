#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/12 下午6:13
# @Author  : wubin
# @Site    : https://www.cnhzz.com
# @File    : automatic_down_node.py
# @Software: PyCharm
# @info    : 实时查看负载，实时自动检测下线。


import urllib2
import urllib
import re
import time
import requests
import datetime
import json
from requests.auth import HTTPBasicAuth

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

req_load_url = "http://ops.intra.knownsec.com/nagios/cgi-bin/archivejson.cgi?"

post_data = {
    "query": "notificationlist",
    "objecttypes": "service",
    "servicenotificationtypes": "critical",
    "servicedescription": "LOAD",
    "starttime": "1481600597",
    "endtime": "1481600597"
}
post_user = {

    "wub": "1QAZzaq1"
}

now_time = datetime.datetime.now()
ago_time = now_time + datetime.timedelta(seconds=-300)

now_time_seconds = int(time.mktime(time.strptime(now_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")))
ago_time_seconds = int(time.mktime(time.strptime(ago_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")))


url_critical = "http://ops.intra.knownsec.com/nagios/cgi-bin/archivejson.cgi?query=notificationlist&objecttypes=service&servicenotificationtypes=critical+warning&servicedescription=LOAD&starttime=%s&endtime=%s" % (
ago_time_seconds, now_time_seconds)


url_recovery = "http://ops.intra.knownsec.com/nagios/cgi-bin/archivejson.cgi?query=notificationlist&objecttypes=service&servicenotificationtypes=recovery&servicedescription=LOAD&starttime=%s&endtime=%s" % (
ago_time_seconds, now_time_seconds)

down_node_post_url = "http://jslyj.jiasule.com/yjsghdf/service_manage/node_config/update/"

cookies_file = open("/root/.sbin/cookie.txt").read().split("\n")[0]
cookies_dict = dict(cookies_are=cookies_file)

node_config_offline = {
        "note":"",
        "node_weight": "1",
        "switch_ids[]": "",
        "csrfmiddlewaretoken": ""
    }

def get_csrftoken_data():
    for i in cookies_file.split(";"):
        if "csrftoken" in i:
            node_config_offline["csrfmiddlewaretoken"] = i.split("=")[1]
    return node_config_offline


get_csrftoken_data()

def get_node_info():
    "获取节点信息，并存入文件"
    node_conf_json = []
    open("/var/tmp/getnodelist.json", "w+")
    for page in range(1, 28):
        node_conf_url = "http://jslyj.jiasule.com/yjsghdf/service_manage/node_config/list/?page=%s" % page
        req = requests.get(node_conf_url, cookies=cookies_dict)
        guize = re.compile(r"node_data\[id\] = (.*);")
        node_conf = guize.findall(req.content)
        node_conf_json.extend(node_conf)
        # f.writelines(node_conf)
        for j in node_conf:
            f = open("/var/tmp/getnodelist.json", "a+")
            fromat_f = "%s\n" % j
            print (j)
            f.writelines(fromat_f)


# 更新节点信息
# print get_node_info()


def get_node_id(node_name):
    "获取节点 id 号"
    read_json = open("/var/tmp/getnodelist.json", "r").readlines()
    node_id = []
    for i in read_json:
        if node_name in eval(i.split("\n")[0])["node_name"]:
            node_id.append(eval(i.split("\n")[0])['id'])
    return node_id


def get_down_node(node_name):
    for nodes_id in get_node_id(node_name):
        get_csrftoken_data()['switch_ids[]'] = nodes_id
        get_csrftoken_data()['note'] = "负载报警，自动下线！by 脚本！%s" % datetime.datetime.now()
        down_req = requests.post(down_node_post_url,data=get_csrftoken_data(),cookies=cookies_dict)
        print down_req.json()['message'],datetime.datetime.now()

def get_recovery_node(node_name):
    for nodes_id in get_node_id(node_name):
        get_csrftoken_data()['switch_ids[]'] = nodes_id
        get_csrftoken_data()['node_weight'] = 50
	get_csrftoken_data()['note'] = "负载恢复，自动上线 by 脚本！%s" % datetime.datetime.now()
        down_req = requests.post(down_node_post_url, data=get_csrftoken_data(), cookies=cookies_dict)
        print down_req.json()['message'],datetime.datetime.now()
# get_down_node("tx-nanchang2-cuc26")

# get_recovery_node("tx-nanchang2-cuc26")

if __name__ == '__main__':
    critical = requests.get(url_critical,auth=HTTPBasicAuth("wub","1QAZzaq1"))
    for i in critical.json()['data']["notificationlist"]:
        if i["contact"] == "zxyy":
            print u"故障机器：%s" % i['host_name']
            get_down_node(i['host_name'].split("200-")[1])

    recovery = requests.get(url_recovery, auth=HTTPBasicAuth("wub", "1QAZzaq1"))
    for i in recovery.json()['data']["notificationlist"]:
        if i["contact"] == "zxyy":
            print u"恢复机器：%s" % i['host_name']
            get_recovery_node(i['host_name'].split("200-")[1])
