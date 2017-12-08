#coding=utf-8
# @Time    : 2017/5/20
# @Author  : liuk
# @Site    : 303donatello
# @File    : examine.py
# @Software: PyCharm
import re
import requests
import threading
def info_read(url,cookies):
    response = requests.get(url=url, cookies=cookies).text
    domain_url = re.findall('data-domain="(.*?)"', response, re.S)
    for each in domain_url:
        print("www." + each)
    print('-----------------------------')
for page in range(1):
    url = 'http://jslyj.jiasule.com/yjsghdf/domain_manage/site/list/?keywords=none&search_type=active_nolaw&page=%s'%page
    cookies = {'Cookie':''}
    cookies_file = open("cookie.txt","r+")
    cookies_real=cookies_file.read()
    cookies['Cookie']=cookies_real
    threading.Thread(target=info_read,args=(url,cookies,)).start()


