# -*- coding: utf-8 -*-

import requests
import re
import json
import subprocess
import csv
import argparse
import os
from bs4 import BeautifulSoup
import sys

jsl_url = "http://jslyj.jiasule.com/yjsghdf"
cookies_file = open('/root/.sbin/cookie.txt','r').read().split("\n")[0]

change_data = {
    'csrfmiddlewaretoken': 'In8SYk0F3Ob2Zj3RbFJNuLZBjEu8GMb7',
    'site_law_value': '0_3',
    'id': '',
    'site_law_type': '',
    'site_group': '47',
    'site_law_note': ''
}

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    'Cookie': ""
}
headers.update(Cookie=cookies_file)

#用户信息
user = sys.argv[1]
keyword = re.sub('@','%40',user)
#页数
page = int(sys.argv[2])+1

urls = ["http://jslyj.jiasule.com/yjsghdf/domain_manage/site/list/?search_type=username&source=&site_belong=&user_group=&keywords={}&group_id=&page={}" .format(keyword,str(i)) for i in range(1,page,1)]

def get_csrftoken():
    for token in headers['Cookie'].split(";"):
        if "csrftoken" in token:
            csrftoken = token.split("=")[1]
            return csrftoken

def change_status():
    change_url = "http://jslyj.jiasule.com/yjsghdf/domain_manage/site/audit/has_group_set/"
    change_session = requests.session()
    change_session.headers = headers
    token = get_csrftoken()
    change_data['csrfmiddlewaretoken'] = token
    change_result = change_session.post(change_url, data=change_data)

def get_id(url):
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    title_list = soup.select('td.ckbox.ckbox_child > input')
    n  = len(title_list)
    if title_list:
        for i in range(0,n,1):
            result = re.split(r'[= "]',str(title_list[i]))[7]
	    change_data['id'] = result
            change_status()
    else:
        pass



if __name__=="__main__":
    for url in urls:
        get_id(url)
