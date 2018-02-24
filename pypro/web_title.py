#coding=utf-8
import urllib.request
from urllib import request
import urllib.error
from bs4 import BeautifulSoup
import datetime
import os
import logging
import requests
import fileinput
import sys
import random
import urllib3.request
import socket

socket.setdefaulttimeout(20)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}

'''my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
    ]'''
#type = sys.getfilesystemencoding()
#print(type)
def get_title():
    i = 0
    if not os.path.exists('D:/webdata/'):
        os.mkdir('D:/webdata/')
#    while True:
#        url=input('enter url: ')
#        urls.append(url)
#        if url=='q'or url=='Q':
#            break
    with open('D:/web.txt','r') as fl:
        urls = fl.read().splitlines()
    #print(urls)
    for url in urls:
        print(url)
        try:
            #headers = random.choice(my_headers)
            urllib3.disable_warnings()
            #http = urllib3.PoolManager()
            #html = http.request('GET',url,headers=headers)
            req = urllib.request.Request(url,headers=headers)
            html = urllib.request.urlopen(req).read()
            #s = requests.session()
            #html = s.get(url,headers=headers,verify=False)
            #print(html)
            soup = BeautifulSoup(html,'lxml')
            titles = soup.find('title')
            print(titles)
            if titles is None:
                with open('D:/webdata/onsure.txt','a') as fil:
                    fil.write('%s\n' %url)
                continue
        except urllib.error.URLError as e:
            logging.basicConfig(filename = 'D:/webdata/log-err.txt',format='%(asctime)s',level = logging.ERROR)
            logging.exception(e)
        except socket.timeout as e:
            logging.basicConfig(filename='D:/webdata/log-err.txt',filemode='a',format='%(asctime)s')
            logging.exception(e)
        else:
            for filter_word in open('D:/test.txt','r'):
                if filter_word.strip() in titles.text:
                    data = {
                        'web': url,
                        'title': titles.text,
                        'info': filter_word
                     }
                    print(data)
                    with open('D:/webdata/urls.txt','a') as fu:
                        fu.write(url+'\n')
                    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
                    with open('D:/webdata/outcome'+now_time+'.txt','a',encoding='gbk',errors='ignore') as f:
                        f.write('%d.\n' %i)
                        f.write('url:'+url+'\n')
                        f.write('title:'+titles.text+'\n')
                        f.write('info:'+filter_word.strip()+'\n')
        print('----'*15)
        i = i + 1
        if i == len(urls) - 1:
            break

if __name__=='__main__':
    get_title()
