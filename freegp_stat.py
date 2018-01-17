#!/usr/local/python36/bin python3
# -*- coding: utf-8 -*-

import sys
import requests
import re
import os
from bs4 import BeautifulSoup
import json

cookies_file = open('/root/.sbin/cookie.txt','r').read().split("\n")[0]
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    'Cookie': ""
}
headers.update(Cookie=cookies_file)

api_url = "http://jslyj.jiasule.com/yjsghdf/domain_manage/site/"

def get_csrftoken():
    for token in headers['Cookie'].split(";"):
        if "csrftoken" in token:
            csrftoken = token.split("=")[1]
            return csrftoken

change_data = {
    'csrfmiddlewaretoken': 'In8SYk0F3Ob2Zj3RbFJNuLZBjEu8GMb7',
    'site_law_value': '0_3',
    'id': '',
    'site_law_type': '',
    'site_group': '0',
    'site_law_note': ''
}

#获取根域名的ID号
def get_id(domain):
    url = '%slist/?keywords=%s&search_type=domain&group_id=&source=&user_group=&site_belong=' % (api_url,domain)
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    title_list = soup.select('td.ckbox.ckbox_child > input')
    if title_list:
        result = re.split(r'[= "]',str(title_list[0]))[7]
        return result
    else:
        pass



#修改域名从合规至违规
def change_status():
    change_url = "http://jslyj.jiasule.com/yjsghdf/domain_manage/site/audit/has_group_set/"
    change_session = requests.session()
    change_session.headers = headers
    token = get_csrftoken()
    change_data['csrfmiddlewaretoken'] = token
    change_data['id'] = groupid
    change_result = change_session.post(change_url, data=change_data)


def search(domain):
    search_session = requests.session()
    search_session.headers = headers
    url = "%slist/?keywords=%s&search_type=domain&group_id=&source=&user_group=&site_belong=" % (api_url,domain)
    active_row = re.compile(r'<td>(.*)</td>')
    out_row = re.compile(r'<font color(.*)</font>')
    group_row = re.compile(r'data-toggle="modal"(.*)</a>')
    search_result = search_session.get(url).text
    active_result = active_row.findall(search_result)
    out_result = out_row.findall(search_result)
    group_result = group_row.findall(search_result)
    group_id = re.split(r'[>-]',group_result[1])[1]
    web_out = re.split(r'[>]',out_result[0])[1]
    web_status = re.split(r'[><]',active_result[5])[2]
    if web_status == 'active' and web_out == u'合规' and group_id == sys.argv[1]:
        change_status()

if __name__== '__main__':
    with open('/root/.sbin/freedomain','r') as f:
        domains = f.read().splitlines()
    for domain in domains:
        groupid = get_id(domain)
	search(domain)
