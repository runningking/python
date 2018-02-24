#coding=utf-8
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import datetime
import os
import logging
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Cookie': 'EDUWEBDEVICE=0568a277f69e47a1834377962e8a77f8; videoResolutionType=3; _ntes_nnid=724da6353c2d9b49ccea517fa18c492a,1510646219036; _ntes_nuid=724da6353c2d9b49ccea517fa18c492a; STUDY_CP_ENTRANCE_CLOSE=1; hasVolume=true; NTES_STUDY_YUNXIN_ACCID=s-1031966865; NTES_STUDY_YUNXIN_TOKEN=bf23d96677a2e95c621fbfd28b0f4328; sideBarPost=502; utm="eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cDovL3N0dWR5LjE2My5jb20vbXk="; NTESSTUDYSI=cd8f70bc0150410594c95020f2aa5794; STUDY_INFO=oP4xHuPyW75RTGm-Zr18xZThVQRo|6|1031966865|1510880916576; STUDY_SESS="ftDspfPt2LOuMgFFOEPEh7CcCgOugqqzdLagE2Uw5A2Q47eBj+9qpdOFy05IWo535EeymIZYX6W3dNxyA5JUPse9ajsXvGpg2feAaWAWSVaUMNcQu8Sh5jm8dtnWD98rKARpmL2BnVPPNjtVX5+k0x6zjp7lY/8vhMkA20t1nn0Lhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="; STUDY_PERSIST="wM9YOiPWjSkFTx+RZ4KfylWMkrzWsLhfiGKkwKDaN03wS9bWkfNICJRxYsPrAzz3My3JnnbwGyJ+qDU4IH4y1GWQuBR3U+BB9JHAWGna0+STjXoq9voSlwsZL9sM8tlsgwUvfljKVFjYsnhAHXoJsC2npWmI8aVqmtGMFvT5HqO4r+5OpClljJmzHnTXaMbyLYts5Lf4kykO1aJvN7C/sI3HU5krB3xEHdOjrdMClNPZgpjCC7Iso4RP9U87vJE8LtaQzUT1ovP2MqtW5+L3Hw+PvH8+tZRDonbf7gEH7JU="; NETEASE_WDA_UID=1031966865#|#1508493489310; videoVolume=1; __utma=129633230.850098235.1510535712.1510818791.1510880363.12; __utmb=129633230.60.9.1510881005761; __utmc=129633230; __utmz=129633230.1510535712.1.1.utmcsr=baidu|utmccn=affiliate|utmcmd=cpc|utmctr=11chongdian-Brand05|utmcct=SEM'
}
url = 'http://study.163.com/'
#web_data = requests.get(url)
web_data = requests.get(url)
soup = BeautifulSoup(web_data.text,'lxml')
titles = soup.find('title')
print(titles)
title_list = soup.select('img.imgPic.j-img')
print(title_list)