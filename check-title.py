# -*- coding:utf-8 -*-

import re,os
import urllib2
import urlparse
import threading
import socket
import Queue
import chardet

import time
socket.setdefaulttimeout(10)
queue= Queue.Queue(0)

done = 0

keywords = [
	'私服',
	'皇冠',
	'博彩',
	'秒赞',
	'传奇',
	'百家乐',
	'魔域',
	'弹弓',
	'外挂',
	'黑客',
	'棋牌',
	'ddos',
	'1\.85',
	'奇迹',
	'完美国际',
	'一条龙',
	'新开',
	'热血江湖',
	'天龙八部',
	'传世',
        '邪恶',
        '按摩',
        '福利',
        '彩票',
        '赌场',
		]

white_root = [
		'.cpp114.com',
		'.58sing.com',
		'.cphi.cn',
		]

def core():
	f = open('wangzhan.txt')
	subdomains = f.readlines()
	f.close()
	
	f = open('result_has_check.txt')
	has_subdomains = f.readlines()
	f.close()
	
	has_subdomains = list(set(has_subdomains))

	has_check = []
	for d in has_subdomains:
		has_check.append(d.strip())


	for sub in subdomains:
		whi = False
		if sub not in has_check:
			sub = sub.strip()
			for white in white_root:
				if sub.endswith(white):
					whi =  True
					break
			if not whi:
				queue.put(sub)

	works = []
	for i in range(80):
		task =Worker(i)
		task.start()
		works.append(task)
	
	for task in works:
		task.join()

	print 'end!!!!'

class Worker(threading.Thread):
	def __init__ (self,index):
		threading.Thread. __init__(self)
		self.index= index
	def run(self):
		while 1:
			global done,white_root
			done+=1
			#if done%300==0:
			#	print done,queue.qsize(),threading.activeCount()
			if queue.qsize() == 0:
				break
			try:
				sub = queue.get(timeout=3)
				getinfo(sub)
			except Exception,e:
				pass
		queue.task_done()


def getinfo(sub):
	global done
	try:
		url = 'http://'+sub
		#html = urllib2.urlopen(url).read()

		request = urllib2.Request(url)
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')
		html = urllib2.urlopen(request,timeout=10).read().lower()
		

		#cmd = 'curl --connect-timeout 10 %s' %url
		#html = os.popen(cmd).read().lower()

		html = deencode(html)

		title_start = html.find('<title')
		title_end = html.find('</title')

		title = html[title_start:title_end]

		for key in keywords:
			if title.find(key) !=-1:
				f=open('results.txt','a+')
				f.write('%s %s\n' %(sub,key))
				f.close()
				print sub,key.decode('utf-8','ignore').encode('gbk','ignore'),queue.qsize()
	except Exception,e:
		f=open('error_open.txt','a+')
		f.write('%s %s\n' %(sub,str(e)))
		f.close()
		#print str(e)
		pass
	if done%20==0:
		print "done:%s   qsize:%s   thread:%s   domain:%s" %(done,queue.qsize(),threading.activeCount(),sub)
	
	f=open('result_has_check.txt','a+')
	f.write('%s\n' %sub)
	f.close()
	


def deencode(html):

	encoding = chardet.detect(html)['encoding'].lower()
	try:	
		if encoding != 'unicode':
			if encoding == 'gb2312':
				encoding = 'gbk'
				html = html.decode(encoding,'ingore').encode('utf-8','ignore')
	except:
		pass
	return html	
	

if __name__ == '__main__':
	core()
