import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import datetime
import os
import logging
import requests

urls=[]
i = 0
if not os.path.exists('E:/webdata/'):
    os.mkdir('E:/webdata/')
while True:
    url=input('enter url: ')
    urls.append(url)
    if url=='q'or url=='Q':
        break
print(len(urls))
for url in urls:
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'lxml')
    titles = soup.find('title')
    print(titles)
    for filter_word in open('E:/test.txt','r'):
        if filter_word.strip() in titles.text:
            data = {
                'web': url,
                'title': titles.text,
                'info': 'Sensitive'
            }
            print(data)
            now_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
            with open('E:/webdata/outcome'+now_time+'.txt','a') as f:
                f.write('%d.\n' %i)
                f.write('url:'+url+'\n')
                f.write('title:'+titles.text+'\n')
                f.write('info:'+filter_word.strip()+'\n')
    i = i + 1
    if i == len(urls) - 1:
        break
