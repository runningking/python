#!/usr/bin/env python
##  Encoding: utf-8
##  Author:luol2@knownsec.com
##  Description:
import commands
import sys
import re
import os
import getopt
def usage():
    print """Usage: getload [option]
            -h,--help               #帮助
            -u <操作用户>       #指定登录节点用户名
            -k <节点验证密钥>    #指定登录节点密钥
            -g <GID>                #组ID
            -n <NODEIP>             #节点IP"""
user = "log"
key = "~/.ssh/knownsec_wub_log"
CMD = "ssh %s@%s -i %s 'cat /proc/loadavg'|awk '{print $1,$2,$3}'"
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hg:n:u:k:',['help'])
except getopt.GetoptError:
    usage()
    sys.exit()

if len(opts) == 0:
    usage()
    sys.exit()

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit()
    elif opt == '-u':
        user = arg
    elif opt == '-k':
        key = arg
    elif opt == '-n':
        print commands.getoutput(CMD%(user, arg, key))
    elif opt == '-g':
        com=commands.getoutput('getnode -g %d --lan'%int(arg))
        iplist=com.split()
        for ip in iplist:
            print "===========%s============"%ip
            print commands.getoutput(CMD%(user, ip, key))
    else:
        usage()
        sys.exit()
