# -*- coding: utf-8 -*-

import subprocess
from threading import Thread
import requests
import re
import os
from bs4 import BeautifulSoup
import sys
import dns.resolver
import Queue

q = Queue.Queue()
num_threads = 4

cookies_file = open('/root/.sbin/cookie.txt','r').read().split("\n")[0]
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    'Cookie': ""
}
headers.update(Cookie=cookies_file)

api_url = "http://jslyj.jiasule.com/yjsghdf"

#dnsurl = "http://jslyj.jiasule.com/yjsghdf/domain_manage/dns/list/?sid=5a37a212eb5fcf2c53aa34ee"

page = int(sys.argv[2])+1
urls = ["{}/service_manage/service_status/list/?group={}&page={}" .format(api_url,sys.argv[1],str(i)) for i in range(1,page,1)]

#获取每个域名所在的页数
def get_page(url):
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    page = soup.select('div.btn-group.pull-right.scanv-pager > a')
    page_num = len(page)
    return page_num

#获取根域名的ID号
def get_id(url):
    url_list = []
    #url = ["{}/service_manage/service_status/list/?group={}&page={}" .format(api_url,sys.argv[1],str(i)) for i in range(1,page,1)]
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    title_list = soup.select('td.ckbox > input')
    if title_list:
	for i in range(0,len(title_list),1):
	    result = title_list[i]['id']
	    dnsurl = "%s/domain_manage/dns/list/?sid=%s" % (api_url,result)
            url_list.append(dnsurl)
    else:
        pass
    return url_list

#获取每个网站下解析IP
#def get_ip(domain):
#    ip_list = []
#    try:
#        ans = dns.resolver.query(domain, 'A')
#    	for i in ans.response.answer:
#            for j in i.items:
#                if isinstance(j, dns.rdtypes.IN.A.A):
#	            ip_list.append(j.address)	
#    except dns.resolver.NoNameservers as e:
#	pass
#    except dns.name.EmptyLabel as e:
#	pass
#    return ip_list

def pingme(i,queue,dosip):
    os.environ['dosip'] = str(dosip)
    while True:
        domain = queue.get()
        os.environ['domain'] = str(domain)
#       ret=subprocess.call('sh /root/.sbin/dping.sh %s %s' %(domain,dosip),shell=True,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT)
	output = os.popen('sh /root/.sbin/dping.sh $domain $dosip')
        if output:
            outvalue = output.read()
	    with open('/root/.sbin/domain_dos','a') as f:
		f.write(outvalue)
	#    break
#        print(ret)
#       if ret == 0:
#           print(domain)
        queue.task_done()


#获取每个域名下每个网站的解析ip
def get_domain(dnsurl):
    result = []
    domain_session = requests.session()
    domain_session.headers = headers
    domain_result = domain_session.get(dnsurl).text
    host_row = re.compile(r'<a title=(.*)</a>')
    domain_row = re.compile(r'<td class=(.*)</td>')
    host_result = host_row.findall(domain_result)
    domain_need = domain_row.findall(domain_result)
    try:
        base_domain = re.split(r'[=\']',domain_need[0])[3]  #根域名
    except IndexError as e:
	pass
    host_num = len(host_result)    #主机名数量
    for i in range(0,host_num,1):
        results = re.split(r'[>]',host_result[i])[1]   #主机名
	domains = results+'.'+base_domain     #要ping的网址
	result.append(domains)
    for i in range(num_threads):
        t=Thread(target=pingme,args=(i,q,ddos_ip))
        t.setDaemon(True)
        t.start() 
    for dom in result:
        q.put(dom)
    q.join


if __name__=="__main__":
    filename = '/root/.sbin/domain_dos'
    if os.path.exists(filename):
        os.system('rm /root/.sbin/domain_dos')
    ddos_ip = sys.argv[3]
    for url in urls:
        url_list = get_id(url)    #分组单页下每个域名对应的链接列表
	for sigl_url in url_list:
	    page_no = get_page(sigl_url)   #在DNS管理中每个域名搜出来的总页数
            if page_no == 0:
	        get_domain(sigl_url)
	    else:
		page_num = int(page_no)+1
		sig_url = ["{}&domain=&point=&page={}" .format(sigl_url,str(i)) for i in range(1,page_num,1)]
		for sigle_url in sig_url:
		    get_domain(sigle_url)

