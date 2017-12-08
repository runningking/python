#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/3 下午2:42
# @Author  : wubin
# @Site    : https://www.cnhzz.com
# @File    : set_ex_group.py
# @Software: PyCharm

import requests
import commands
import sys

var_path = "/root/.sbin"
cookies_path = "%s/cookie.txt" % var_path
reurl = "http://jslyj.jiasule.com/yjsghdf/site/list/"
Cookie = open(cookies_path, 'r').read().split("\n")[0]
cookies_dict = dict(cookies_are=Cookie)

headers_dict = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0',
                'X-CSRFToken': "",
                'Cookie': Cookie
          }

def get_headers_csrftoken():
    f = open(cookies_path, 'r').read().split(";")
    for i in f:
        if "csrftoken" in i:
            csrftoken = str(i).split("=")[1].split("\n")[0]
            headers_dict['X-CSRFToken'] = csrftoken
            return headers_dict


headers_str = get_headers_csrftoken()

ex_group_data = {
    'current_site_id':'56331ed3df224f7ed2d4d5aa',
    'ex_gid':'401',
    'expire_time':'24'
}

ex_group_data['ex_gid'] = sys.argv[2]
if __name__ == '__main__':
    cmd_str = "%s/chgroup.py -g %s --list | awk '{print $1,$2}'" % (var_path,sys.argv[1])
    domain_id_list = commands.getoutput(cmd_str)
    set_ex_group_url = "http://jslyj.jiasule.com/yjsghdf/domain_manage/site/set_ex_group/"
    for domain_id in domain_id_list.split('\n'):
        ex_group_data['current_site_id'] = domain_id.split()[0]
        requests_session = requests.post(set_ex_group_url,data=ex_group_data,headers=headers_str)
        #print u"%s 从%s组扩展配置到%s %s" % (sys.argv[1],sys.argv[2],domain_id.split()[1],requests_session.json()['message'])
        print u"域名:%s 从『%s』扩展配置到『%s』%s" %(domain_id.split()[1],sys.argv[1],sys.argv[2],requests_session.json()['message'])
