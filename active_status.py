#!/usr/local/python36/bin python3
# -*- coding: utf-8 -*-

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
    'site_law_value': '1',
    'id': '',
    'site_law_type': '',
    'site_group': '0',
    'site_law_note': 'ceshi'
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
   # get_session = requests.session()
   # get_session.headers = headers
   # get_result = get_session.get(url).text
   # id_row = re.compile(r'<td>(.*)</td>')
   # id_result = re.split(r'[ =]',id_row.findall(get_result)[5])[4]
   # return id_result

#修改域名从违规至合规
def change_status():
    change_url = "http://jslyj.jiasule.com/yjsghdf/domain_manage/site/audit/has_group_set/"
    change_session = requests.session()
    change_session.headers = headers
    token = get_csrftoken()
    change_data['csrfmiddlewaretoken'] = token
    change_result = change_session.post(change_url, data=change_data)

#获取批量域名
domian_file = '/root/.sbin/批量套餐信息整理.csv'
cmd_file = "awk -F ',' '{print $1}' 批量套餐信息整理.csv|tail -n +2 > /root/.sbin/domainfile"
os.system(cmd_file)


def search(domain):
    search_session = requests.session()
    search_session.headers = headers
    url = "%slist/?keywords=%s&search_type=domain&group_id=&source=&user_group=&site_belong=" % (api_url,domain)
    active_row = re.compile(r'<td>(.*)</td>')
    out_row = re.compile(r'<font color(.*)</font>')
    search_result = search_session.get(url).text
    active_result = active_row.findall(search_result)
    out_result = out_row.findall(search_result)
    web_out = re.split(r'[>]',out_result[0])[1]
    web_status = re.split(r'[><]',active_result[5])[2]
    if web_status == 'active' and web_out == u'违规':
        change_status()

#获取域名创建时间
def search_time(domain):
    time_session = requests.session()
    time_session.headers = headers
    url = "%slist/?keywords=%s&search_type=domain&group_id=&source=&user_group=&site_belong=" % (api_url,domain)
    time_row = re.compile(r'<td title=(.*)</td>')
    time_result = time_session.get(url).text
    create_result = time_row.findall(time_result)
    create_time = re.split('[:" ]',create_result[0])[1]
    start_time = create_time.encode('utf-8',errors='ignore')
    print(domain)
    print(start_time+'\n')

if __name__== '__main__':
    with open('/root/.sbin/domainfile','r') as f:
        domains = f.read().splitlines()
    for domain_list in domains:
        sid = get_id(domain_list)
        change_data['id'] = sid
	search(domain_list)
	search_time(domain_list)

