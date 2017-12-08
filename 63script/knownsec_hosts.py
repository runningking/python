#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/6 下午2:01
# @Author  : wubin
# @Site    : https://www.cnhzz.com
# @File    : api.py
# @Software: PyCharm

import redis

import socket
import socks
import re
import json
import sys

DBINFO = {
    'host': '120.12.30.15',
    'password': '2d3l3fp28p7d24p9e1l06p3aappa4dd2m10e628m',
    'port': 6383}


#socks.set_default_proxy(socks.SOCKS5,addr='127.0.0.1',port=7070)
#socket.socket = socks.socksocket

DBINFO['password'] = DBINFO['password'].replace('l', 'b').replace('p', '5').replace('m', 'c')
DBINFO['host'] = DBINFO['host'].replace('120.', '10.').replace('.12.', '.10.').replace('.30.', '.3.').replace('.15',
                                                                                                              '.1')
if __name__ == '__main__':

    read_redis = redis.Redis(host=DBINFO['host'],db=1,port="6383",password=DBINFO['password'])
    group_list = []
    # set_group = "group_%s" % (sys.argv[1])
    {}.iteritems()
    for group_id in read_redis.keys():
        # # print x,y
        # if "service_sites" not in x:
        #     node_name = x
        #     node_info = json.loads(y)
        #     # print node_name,node_info.values()[2]
        #     group_list.append(node_info.values()[2])
        # print group_id
        # print read_redis.type(group_id)
        # if read_redis.type(group_id) == 'set':
        #     print group_id
        group_ip_list = []
        if read_redis.type(group_id) == 'hash':
            for group_idc_name,group_ip in read_redis.hgetall(group_id).iteritems():
                if "service_sites" not in group_idc_name:
                    group_ip_str = json.loads(group_ip )['ip']
                    group_ip_list.append(group_ip_str)
                    # print group_id,group_idc_name,json.loads(group_ip )['ip']

            hostlist = {group_id: group_ip_list}
            print json.dumps(hostlist)
    # group_id = sys.argv[1]
    # hostlist = {group_id: group_list}
    # # print json.dumps(hostlist)
    # print hostlist
