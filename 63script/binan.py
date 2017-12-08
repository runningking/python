#!/usr/bin/env python
#  Encoding: utf-8
#  Author:luol2@knownsec.com
#  Description:
from __future__ import division
import threading
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
    [核心参数]
    -i <id>             #将指定域名ID切换致指定分组.
    -g <gid>            #指定分组ID
    [组合参数]
    --list              #显示分组域名列表
    --cn                #使用国内检测分组
    --hk                #使用香港检测分组
    --check             #首次检测
    --recheck           #继续检测攻击分组
"""


def change_group():
    """调用变更分组接口
    """
    while 1:
        try:
            id_grp = CHANGE_GRP_LIST.pop()
            domain_id = id_grp[0]
            group = id_grp[1]
            chg_dm_grp(domain_id, group)
            # time.sleep(1)
        except:
            break


def progress_bar():
    """打印执行进度条
    """
    while 1:
        NOWNUM = len(CHANGE_GRP_LIST)
        if NOWNUM != 0:
            COMNUM = int(IDLEN - NOWNUM)
            COMPER = int(COMNUM / IDLEN * 100)
            j = "#" * COMPER
            sys.stdout.write(str(COMPER) + '% ||' + j + '->' + "\r")
            sys.stdout.flush()
            time.sleep(0.5)
        else:
            j = "#" * 100
            sys.stdout.write('100' + '% ||' + j + '->' + "\r")
            break
    print


def start_change_grp():
    """并发调用变更分组接口
    """
    threadsize = 30
    threads = list()
    for i in xrange(threadsize):
        threads.append(threading.Thread(target=change_group, args=()))
    threads.append(threading.Thread(target=progress_bar, args=()))
    for Thread in threads:
        Thread.start()
    for Thread in threads:
        Thread.join()


def get_grp_domains(gid):
    """获取指定分组域名数据
    """
    # API_HOST = 'http://test-ui1-ht.intra.jiasule.com'
    API_HOST = 'http://jslyj.jiasule.com'
    AUTH = 'lrKNOuscF7CKFAiLyAzxUumlAZEVr7SNogR2EbKE6jA'
    GROUP_ID = gid
    PWD_OBJ = urllib2.HTTPPasswordMgrWithDefaultRealm()
    API_URL = "%s/api/?type=query_group&group=%s" % (API_HOST, GROUP_ID)
    PWD_OBJ.add_password(None, API_URL, AUTH, '')
    handler = urllib2.HTTPBasicAuthHandler(PWD_OBJ)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    wp = urllib2.urlopen(API_URL)
    data = json.loads(wp.read())
    return data['ret']


def chg_dm_grp(idnum, gid):
    """设置变更分组调用接口
    """
    API_HOST = 'http://jslyj.jiasule.com'
    AUTH = 'lrKNOuscF7CKFAiLyAzxUumlAZEVr7SNogR2EbKE6jA'
    GROUP_ID = gid
    DOMAIN_ID = idnum
    PWD_OBJ = urllib2.HTTPPasswordMgrWithDefaultRealm()
    API_URL = "%s/api/?type=modify_group&id=%s&group=%s" % (API_HOST, DOMAIN_ID, GROUP_ID)
    PWD_OBJ.add_password(None, API_URL, AUTH, '')
    handler = urllib2.HTTPBasicAuthHandler(PWD_OBJ)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    wp = urllib2.urlopen(API_URL)
    data = json.loads(wp.read())
    return data['status']


def restore_group(gid):
    """将没攻击的组还原
    """
    global CHANGE_GRP_LIST
    global IDLEN
    CHANGE_GRP_LIST = list()
    dm_num = 0
    domains = json.load(open(DOMAIN_FILE, 'r'))
    for dminfo in domains:
        if dminfo['last_gid'][-1] != gid and dminfo['status'] == 'checking':
            CHANGE_GRP_LIST.append([dminfo['id'], dminfo['last_gid'][0]])
        elif dminfo['last_gid'][-1] == gid and dminfo['status'] == 'checking':
            dm_num += 1
    IDLEN = len(CHANGE_GRP_LIST)
    print "正将没有攻击嫌疑的域名还原至%s号分组" % dminfo['last_gid'][0]
    start_change_grp()
    return domains, dm_num


def get_dmlist(gid):
    """显示分组域名列表
    """
    data = get_grp_domains(gid)
    # for dm in data:
    #     print dm,data[dm]['id'],VERSION[data[dm]['vip'].values()[0]['name']]
    for key, values in data.iteritems():
        if len(values['vip']) == 1:
            print data[key]['id'], key, VERSION[values['vip'][values['vip'].keys()[0]]['name']]
        elif len(values['vip']) == 2:
            print data[key]['id'], key, VERSION[values['vip'][values['vip'].keys()[0]]['name']], VERSION[
                values['vip'][values['vip'].keys()[1]]['name']]
        elif len(values['vip']) == 3:
            print data[key]['id'], key, VERSION[values['vip'][values['vip'].keys()[0]]['name']], VERSION[
                values['vip'][values['vip'].keys()[1]]['name']], VERSION[values['vip'][values['vip'].keys()[2]]['name']]


def check_attack_domain(obj_gid, area, chk_type):
    """将分组域名平分配到攻击检测组
    """
    global CHANGE_GRP_LIST
    global IDLEN
    CHANGE_GRP_LIST = list()
    if chk_type == 'recheck':
        if os.path.exists(DOMAIN_FILE):
            data, dm_num = restore_group(obj_gid)
        else:
            print "必须先进行先使用--check选项进行首次检测."
            sys.exit(3)

    if chk_type == 'check':
        if not os.path.exists(DOMAIN_FILE):
            data = get_grp_domains(obj_gid)
            dm_num = len(data)
        else:
            print "本地已经存在检测首次检测文件[%s]，请使用--recheck继续检测，或备份检测文件重新检测." % DOMAIN_FILE
            sys.exit(3)

    if area == 'cn':
        grplist = cn_chkattack_grp
    else:
        grplist = hk_chkattack_grp

    grp_num = len(grplist)
    print "===================================="
    print "域名数:%s 检测分组数:%s" % (dm_num, grp_num)
    if dm_num > grp_num:
        if dm_num % grp_num == 0:
            sep_num = dm_num / grp_num
        else:
            sep_num = dm_num / grp_num + 1
    else:
        sep_num = 1
    print "每个分组域名数:%s" % int(sep_num)
    print "===================================="
    sep = 0
    gid = grplist.pop()

    for dm in data:
        if chk_type == 'recheck':
            if dm['last_gid'][-1] != obj_gid or dm['status'] == 'complet':
                dm['status'] = 'complet'
                DOMAIN_LIST.append(dm)
                continue
        if sep >= sep_num:
            try:
                gid = grplist.pop()
                sep = 1
            except:
                pass
        else:
            sep += 1

        if chk_type == 'check':
            domain = dm
            domain_id = data[domain]['id']
            DOMAIN_LIST.append({'domain': dm, 'id': domain_id, 'status': 'checking', 'last_gid': [obj_gid, gid]})
        else:
            domain = dm['domain']
            domain_id = dm['id']
            last_gid = dm['last_gid']
            last_gid.append(gid)
            dminfo = {'domain': domain, 'id': domain_id, 'last_gid': last_gid, 'status': 'checking'}
            DOMAIN_LIST.append(dminfo)

        CHANGE_GRP_LIST.append([domain_id, gid])
        IDLEN = len(CHANGE_GRP_LIST)

    json.dump(DOMAIN_LIST, open(DOMAIN_FILE, 'w'))
    print "正将有攻击嫌疑的域名分发至攻击验证分组中"
    start_change_grp()


def main(argv):
    global DMID
    DMID = None
    try:
        opts, args = getopt.getopt(argv[1:], 'g:i:', ['group=', 'list', 'hk', 'cn', 'check', 'recheck'])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    ops = dict(opts).keys()
    for o, a in opts:
        if o in ('-i',):
            DMID = a

        if o in ('-g', '--group'):
            GID = int(a)

            if not DMID is None:
                chg_dm_grp(DMID, GID)
                print "已将(ID: %s)对应域名变更至:%s号分组." % (DMID, GID)
                sys.exit(1)

            if '--list' in ops:
                get_dmlist(GID)
                sys.exit(0)

            if '--cn' in ops:
                AREA = 'cn'
            elif '--hk' in ops:
                AREA = 'hk'
            else:
                print "[ERR]请指定检测分组类型(--cn/--hk).\n"
                Usage()
                sys.exit(1)

            if '--check' in ops:
                TYPE = 'check'
            elif '--recheck' in ops:
                TYPE = 'recheck'
            else:
                print "[ERR]请指定检测类型(--check/--rechke).\n"
                Usage()
                sys.exit(1)

            check_attack_domain(GID, AREA, TYPE)


if __name__ == '__main__':

    VERSION = {
        'free': u"免费版",
        'vip11': u"标准版",
        'vip1111': u"专属套餐",
        'vip12': u"专业版",
        'vip13': u"高性能版",
        'vip21': u"CDN普通版",
        'vip22': u"抗D保旗舰版",
        'vip23': u"抗D保豪华版",
        'vip98': u"CDN政企版",
        'vip99': u"政企版",
        'vip_cyd_online': u"创宇盾线上版",
        'vip_cyd_expire': u"创宇盾试用版过期",
        'vip_cyd_free': u"创宇盾试用版",
        'vip_cyd_pro': u"创宇盾旗舰版",
        'vip_cyd_signed': u"创宇盾基础版",
        'vip_cyd_upper': u"创宇盾高级版",
        'vip_kdb_c10': u"KDB-C10",
        'vip_kdb_c100': u"KDB-C100",
        'vip_kdb_c5': u"KDB-C5",
        'vip_kdb_c50': u"KDB-C50",
        'vip_kdb_d10': u"KDB-D10",
        'vip_kdb_d120': u"KDB-D120",
        'vip_kdb_d20': u"KDB-D20",
        'vip_kdb_d300': u"KDB-D300",
        'vip_kdb_d50': u"KDB-D50",
        'vip_kdb_d500':u"KDB-500",
        'vip_kdb_d80': u"KDB-D80",
        'vip_kdb_d800': u'KDB-D800'
    }
    DOMAIN_FILE = '/var/tmp/chkattack.json'
    DOMAIN_LIST = list()
    hk_chkattack_grp = [73, 74, 75, 76, 77]
    cn_chkattack_grp = [78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                        101, 102, 103, 104, 105, 106, 107]
    if len(sys.argv) == 1:
        Usage()
        sys.exit(3)
    main(sys.argv)
