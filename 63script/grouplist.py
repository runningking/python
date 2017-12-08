#!/usr/bin/env python
#  Encoding: utf-8
#  Author:luol2@knownsec.com
#  Description:
from __future__ import division
import urllib2
import getopt
import time
import json
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')


def Usage():
    print """语法： chgroup [参数] ...

功能描述：域名分组切换

参数说明：
    -g <gid>            #指定分组ID
"""

VERSION = {
                'free':u"免费版",
                'vip11':u"标准版",
                'vip1111':u"专属套餐",
                'vip12':u"专业版",
                'vip13':u"高性能版",
                'vip21':u"CDN普通版",
                'vip22':u"抗D保旗舰版",
                'vip23':u"抗D保豪华版",
                'vip98':u"CDN政企版",
                'vip99':u"政企版",
                'vip_cyd_expire':u"创宇盾试用版过期",
                'vip_cyd_online':u"创宇盾线上版",
                'vip_cyd_free':u"创宇盾试用版",
                'vip_cyd_pro':u"创宇盾旗舰版",
                'vip_cyd_luxury':u"创宇盾豪华版",
                'vip_cyd_signed':u"创宇盾基础版",
                'vip_cyd_upper':u"创宇盾高级版",
                'vip_kdb_c10':u"KDB-C10",
                'vip_kdb_c100':u"KDB-C100",
                'vip_kdb_c5':u"KDB-C5",
                'vip_kdb_c50':u"KDB-C50",
                'vip_kdb_d10':u"KDB-D10",
                'vip_kdb_d120':u"KDB-D120",
                'vip_kdb_d20':u"KDB-D20",
                'vip_kdb_d300':u"KDB-D300",
                'vip_kdb_d50':u"KDB-D50",
                'vip_kdb_d80':u"KDB-D80"
}

def get_grp_domains(gid):
    """获取指定分组域名数据
    """
    GROUP_ID = gid
    API_HOST = 'http://jslyj.jiasule.com'
    PWD_OBJ = urllib2.HTTPPasswordMgrWithDefaultRealm()
    AUTH = 'lrKNOuscF7CKFAiLyAzxUumlAZEVr7SNogR2EbKE6jA'
    API_URL = "%s/api/?type=query_group&group=%s" % (API_HOST, GROUP_ID)
    PWD_OBJ.add_password(None, API_URL, AUTH, '')
    handler = urllib2.HTTPBasicAuthHandler(PWD_OBJ)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    wp = urllib2.urlopen(API_URL)
    data = json.loads(wp.read())
    return data['ret']

def get_dmlist(gid):
    """显示分组域名列表
    """
    data = get_grp_domains(gid)
    for dm in data:
        print dm,data[dm]['id'],VERSION[data[dm]['vip'].values()[0]['name']]

def main(argv):
    global DMID
    DMID = None
    try:
        opts, args = getopt.getopt(argv[1:], 'g:')
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    ops = dict(opts).keys()
    for o, a in opts:
        if o in ('-g',):
            GID = int(a)
            get_dmlist(GID)
            sys.exit(0)
        else:
            Usage()
            sys.exit(1)

if __name__ == '__main__':

    if len(sys.argv) == 1:
        Usage()
        sys.exit(3)
    main(sys.argv)
