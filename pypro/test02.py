#coding=utf-8
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import datetime
import os
import logging


if not os.path.exists('D:/webdata/'):
    os.mkdir('D:/webdata/')
with open('D:/web.txt','r') as fl:
    urls = fl.readlines()
print(len(urls))
for url in urls:
    print(url)