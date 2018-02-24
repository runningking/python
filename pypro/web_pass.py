#!/usr/local/python36/bin python3
#coding=utf-8
import requests
import re
import os
import json
from bs4 import BeautifulSoup
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    'Cookie': ""
}

headers.update(Cookie=cookies)

def search(domain):
    search_session = requests.session()
    search_session.headers = headers
    url = "http://jslyj.jiasule.com/yjsghdf/domain_manage/site/list/?keywords=%s&search_type=domain&group_id=&source=&user_group=&site_belong=" % (domain)
    active_row = re.compile(r'<td>(.*)</td>')
    search_result = search_session.get(url).text
    active_result = active_row.findall(search_result)
    result = re.split(r'[><]',active_result[8])[2]
    print(result)
   # web_status = re.split(r'[:" ]',active_result[0])[1]

if __name__== '__main__':
    search('80031188.com')
