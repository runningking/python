#coding=utf-8
import sys
import os
import fileinput
import re


#myaddr=os.popen("ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
myaddr,redisversion,redisport=sys.argv[1].split('_')
if len(sys.argv) < 1:
    print '''
                                          参数不全,请参照如下案例设定参数，如有特殊需求，请联系相关人员给予帮助：
            redis.py myaddr_redisversion_redisport1:redisport2:redisport3……(redis版本号_端口列表)
    若无需特殊指定，端口请写0！
            '''
print '''
**********************************
根据入参定义定义redis版本,集群服务器及端口，默认只为本机，
端口7000,7001,7002,7003,7004,7005
***********************************
'''
def createcluster(clusterdir,clusterport):
    clusterport=str(clusterport)
    cmd_mkcluster='mkdir -p %s/%s' % (clusterdir,clusterport)
    os.system(cmd_mkcluster)
    cmd_cpredisconf='cp /opt/redis-%s/redis.conf %s/%s' % (redisversion,clusterdir,clusterport)
    os.system(cmd_cpredisconf)
    filename='%s/%s/redis.conf' % (clusterdir,clusterport)
    print filename
    for line in fileinput.input(filename,inplace=1):
        portrestr='port %s' % (clusterport)
        print re.sub(r'^port 6379',portrestr,line.rstrip())
    for line in fileinput.input(filename,inplace=1):
        print re.sub(r'^protected-mode yes','protected-mode no',line.rstrip())
    for line in fileinput.input(filename,inplace=1):
        bindstr='#bind %s' % (myaddr)
        print re.sub(r'^bind 127.0.0.1',bindstr,line.rstrip())
    for line in fileinput.input(filename,inplace=1):
        print re.sub(r'^daemonize no','daemonize yes',line.rstrip())
    for line in fileinput.input(filename,inplace=1):
        print re.sub(r'^pidfile /var/run/redis_6379.pid','pidfile /var/run/redis_%s.pid' % (clusterport),line.rstrip())
    for line in fileinput.input(filename,inplace=1):
        print re.sub(r'^# cluster-enabled yes','cluster-enabled yes',line.rstrip())
    for line in fileinput.input(filename,inplace=1):
        print re.sub(r'^# cluster-config-file nodes-6379.conf','cluster-config-file nodes-%s.conf' % (clusterport),line.rstrip())
    for line in fileinput.input(filename,inplace=1):    
        print re.sub(r'^appendonly no','appendonly yes',line.rstrip())
    cmd_startredisserver='redis-server %s/%s/redis.conf' % (clusterdir,clusterport)
    os.system(cmd_startredisserver)
    
print '*************下载并解压redis***************'
os.chdir('/opt')
cmd_redisdownload='wget http://download.redis.io/releases/redis-%s.tar.gz' % (redisversion)
os.system(cmd_redisdownload)
cmd_tarredis='tar -xvzf redis-%s.tar.gz' % (redisversion)
os.system(cmd_tarredis)

print '''
********************************************************
    检查初始化环境gcc,ruby,rubygems,ruby&redis interface是否安装！

*********************************************************
    '''
os.system('yum install -y gcc')
os.system('yum install ruby')
os.system('yum install rubygems')
os.system('gem install redis --version 3.0.0')

print '************编译redis*************'
cmd_cdredisroot='/opt/redis-%s' % (redisversion)
os.chdir(cmd_cdredisroot)
os.system('make && make install')
cmd_cpredistrib='cp /opt/redis-%s/src/redis-trib.rb /usr/local/bin/' % (redisversion)
os.system(cmd_cpredistrib)
if redisport=='0':
    for portlist in range(7000,7006):
        createcluster('/opt/redis_cluster', portlist)
    cmd_createcluster='redis-trib.rb create --replicas 1 %s:7000 %s:7001  %s:7002 %s:7003  %s:7004  %s:7005' % (myaddr,myaddr,myaddr,myaddr,myaddr,myaddr)
    print '请在终端服务器执行如下命令后完成redis集群部署：\n%s' % (cmd_createcluster)
    
else:      
    for portlist in redisport.split(':'): 
        createcluster('/opt/redis_cluster', portlist)
    if len(redisport.split(':'))==6:
        cmd_createcluster='redis-trib.rb create --replicas 1 %s:%s %s:%s  %s:%s %s:%s  %s:%s  %s:%s' % (myaddr,redisport.split(':')[0],myaddr,redisport.split(':')[0],myaddr,redisport.split(':')[0],myaddr,redisport.split(':')[0],myaddr,redisport.split(':')[0],myaddr,redisport.split(':')[0])
        os.system(cmd_createcluster)
    else:
        print '''
        请根据服务器部署情况执行以下命令（若多台服务器需要在多台上执行此脚本）：
        redis-trib.rb  create  --replicas  1  192.168.31.245:7000 192.168.31.245:7001  192.168.31.245:7002 192.168.31.210:7003  192.168.31.210:7004  192.168.31.210:7005
        '''
        
    



