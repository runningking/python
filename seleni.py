from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from time import sleep
import sys
import time

with open('D:/server.txt','r') as f:
    servers = f.read().splitlines()

#browser = webdriver.Chrome()
#wait = WebDriverWait(browser,timeout=20)

def search(url):
    browser.get(url)
    email = WebDriverWait(browser,timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > grafana-app > div.main-view > div > div > div.login-inner-box > form > div:nth-child(1) > input')),message=u'元素加载超时!')
    email.send_keys("jinwq")
    passwd = WebDriverWait(browser,timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#inputPassword')),message=u'元素加载超时!')
    passwd.send_keys("Admin+1234")
    submit = WebDriverWait(browser,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > grafana-app > div.main-view > div > div > div.login-inner-box > form > div.gf-form-button-row > button')))
    submit.click()

def get_mata():
    summin = 0
    flowmin = []
    summax = 0
    flowmax = []
    sumavg = 0
    flowavg = []
    sumcur = 0
    flowcur = []
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > grafana-app > div.main-view > div > div > dash-row > div > div:nth-child(2) > plugin-component > panel-plugin-graph > grafana-panel > div > div.panel-content > ng-transclude > div.graph-wrapper > div.graph-legend-wrapper > section')))
    html = browser.page_source
    doc = pq(html)
    for data in doc('.graph-legend-value.min'):
        minum = pq(data).text()
        flowmin.append(minum)
    length = len(flowmin)
    min_num = int(length/2)
    for i in range(0,min_num,1):
        unit = flowmin[i][-4:]
        if unit == "Mbps":
            outvalue = float(flowmin[i][:-4])
            summin += outvalue
        elif unit == "Gbps":
            outvalue = float(flowmin[i][:-4])*1000
            summin += outvalue
        elif unit == "kbps":
            outvalue = float(flowmin[i][:-4])/1000
            summin += outvalue
    with open('D:/result.txt','a') as file:
        file.write('机房出口最小流量和：%s Mbps' % str(summin)+'\n')
    print('机房出口最小流量和：%s Mbps' % summin)

    #出口方向最大流量和
    for data in doc('.graph-legend-value.max'):
        maxnum = pq(data).text()
        flowmax.append(maxnum)
    length = len(flowmax)
    max_num = int(length/2)
    for i in range(0,max_num,1):
        unit = flowmax[i][-4:]
        if unit == "Mbps":
           # print(flowmax[i][:-4])
            outvalue = float(flowmax[i][:-4])
            summax += outvalue
        elif unit == "Gbps":
            #print(flowmax[i][:-4])
            outvalue = float(flowmax[i][:-4])*1000
            summax += outvalue
        elif unit == "kbps":
            outvalue = float(flowmax[i][:-4])/1000
            summax += outvalue
    with open('D:/result.txt','a') as file:
        file.write('机房出口最大流量和：%s Mbps' % str(summax)+'\n')
    print('机房出口最大流量和：%s Mbps' % summax)

    #出口方向平均流量和
    for data in doc('.graph-legend-value.avg'):
        avgnum = pq(data).text()
        flowavg.append(avgnum)
    length = len(flowavg)
    avg_num = int(length/2)
    for i in range(0,avg_num,1):
        unit = flowavg[i][-4:]
        if unit == "Mbps":
            outvalue = float(flowavg[i][:-4])
            sumavg += outvalue
        elif unit == "Gbps":
            outvalue = float(flowavg[i][:-4])*1000
            sumavg += outvalue
        elif unit == "kbps":
            outvalue = float(flowavg[i][:-4])/1000
            sumavg += outvalue
    with open('D:/result.txt','a') as file:
        file.write('机房出口平均流量和：%s Mbps' % str(sumavg)+'\n')
    print('机房出口平均流量和：%s Mbps' % sumavg)

    #出口方向当前流量和
    for data in doc('.graph-legend-value.current'):
        curnum = pq(data).text()
        flowcur.append(curnum)
    length = len(flowcur)
    cur_num = int(length/2)
    for i in range(0,cur_num,1):
        unit = flowcur[i][-4:]
        if unit == "Mbps":
            outvalue = float(flowcur[i][:-4])
            sumcur += outvalue
        elif unit == "Gbps":
            outvalue = float(flowcur[i][:-4])*1000
            sumcur += outvalue
        elif unit == "kbps":
            outvalue = float(flowcur[i][:-4])/1000
            sumcur += outvalue
    with open('D:/result.txt','a') as file:
        file.write('机房出口当前流量和：%s Mbps' % str(sumcur)+'\n')
    print('机房出口当前流量和：%s Mbps' % sumcur)

if __name__=="__main__":
    start_time = int(time.mktime(time.strptime(sys.argv[1],"%Y %m %d"))*1000)
    end_time = int(time.mktime(time.strptime(sys.argv[2],"%Y %m %d"))*1000)
    for server in servers:
        with open('D:/result.txt','a') as file:
            file.write('--------%s--------- ' % server + '\n')
        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, timeout=20)
    #url = 'http://influxdb.intra.jiasule.com:3000/dashboard/db/ji-fang-liu-liang?refresh=1m&orgId=2&from=now-1h&to=now&var-idc=tx-xiangyang-cmc&var-interval=5m'
        url = "http://influxdb.intra.jiasule.com:3000/dashboard/db/ji-fang-liu-liang?orgId=2&from=%s&to=%s&var-idc=%s&var-interval=5m" %(end_time,start_time,server)
        print(url)
        search(url)
        get_mata()
        browser.close()
