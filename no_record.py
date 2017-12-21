#!/usr/local/python36/bin python3
#coding=utf-8
import requests
import re
import os
import json
from bs4 import BeautifulSoup

cookies_file = open('/root/.sbin/cookie.txt','r').read().split("\n")[0]
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    'Cookie': ""
}

headers.update(Cookie=cookies_file)

record = []
group_id = [3,13,19,39,58,68,501,46,31,32,553,519,521,555,522,556,557,567,592,566,521,575,604]
            
def search(domain):
    search_session = requests.session()
    search_session.headers = headers
    url = "http://jslyj.jiasule.com/yjsghdf/domain_manage/site/list/?keywords=%s&search_type=domain&group_id=&source=&user_group=&site_belong=" % (domain)
    active_row = re.compile(r'<td>(.*)</td>')
    search_result = search_session.get(url).text
    active_result = active_row.findall(search_result)
    try:
        result_one = re.split(r'[><]',active_result[8])[2]
        result_id = result_one.split('-')[0]
        print(domain)
        print(result_one+'\n')
	if int(result_id) in group_id:
	    pass
	else:
            record.append(domain)
    except IndexError:
        print(domain)
        print('域名未接入后台'+ '\n')

if __name__== '__main__':
    with open('/root/.sbin/recordfile','r') as f:
        domains = f.read().splitlines()
    for domain in domains:
    	search(domain)
    print('需要核实有无备案域名：')
    print(record)
