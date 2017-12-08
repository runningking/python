#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/29 下午10:31
# @Author  : wubin
# @Site    : https://www.cnhzz.com
# @File    : ptyy_finance.py
# @Software: PyCharm

import requests
from datetime import datetime
import time
import codecs
import csv
import sys
import re
import json
from prettytable import PrettyTable

var_path = "/root/.sbin"
vip_csv_path = "%s/批量套餐信息整理.csv" % var_path
app_csv_path = "%s/批量流量清理.csv" % var_path
coo_file_path = "%s/cookie.txt" % var_path
cookies_file = open(coo_file_path).read().split("\n")[0]
cookies_dict = dict(cookies_are=cookies_file)

api_url = "http://jslyj.jiasule.com/yjsghdf"
#api_url = "http://test-ui1-ht.intra.jiasule.com/yjsghdf"

# 请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0",
    'Cookie': ""
}
# 放Cookie到 headers 里面
headers.update(Cookie=cookies_file)


def get_csrftoken():
    """
    获取 cookies 的 csrftoken
    :return:
    """
    for token in headers['Cookie'].split(";"):
        if "csrftoken" in token:
            csrftoken = token.split("=")[1]
            return csrftoken


# print get_csrftoken()

# 添加套餐的POST 数据
vip_add_data = {
    'trade_product': 'cdn:vip98,ddos:vip_kdb_d50,waf:vip_cyd_pro',
    'trade_user': 'wub@knownsec.com',
    'trade_domain': 'cnhzz.com',
    'trade_amount': '1',
    'trade_unit': 'month',
    'trade_money': '0',
    'note': '吴彬测试',
    'vip_status': 'present'
}

# 添加流量包 POST 数据
app_add_data = {
    'trade_product': 'app_bandwidth',
    'trade_user': 'wub@knownsec.com',
    'trade_domain': 'cnhzz.com',
    'trade_amount': "1",
    'trade_money': '0',
    'vip_status': 'present',
    'note': '吴彬测试'
}

vip_setting_data = {
    'trade_id': '58660d9d4dcc1d55f0488e94',
    'trade_status': 'TRADE_SUCCESS',
    'trade_money': '0.0',
    'expire_time': '2016-12-31+15:32:45',
    'supporter': "",
    "site_belong": "",
    "site_type": "",
    "note": "",
}

trade_product_data = {
    "vip21": "CDN普通版",
    "vip98": "CDN政企版",
    "vip22": "抗D保旗舰版",
    "vip23": "抗D保豪华版",
    "vip_kdb_c10": "KDB-C10",
    "vip_kdb_c100": "KDB-C100",
    "vip_kdb_c5": "KDB-C5",
    "vip_kdb_c50": "KDB-C50",
    "vip_kdb_d10": "KDB-D10",
    "vip_kdb_d120": "KDB-D120",
    "vip_kdb_d20": "KDB-D20",
    "vip_kdb_d300": "KDB-D300",
    "vip_kdb_d50": "KDB-D50",
    "vip_kdb_d500": "KDB-D500",
    "vip_kdb_d80": "KDB-D80",
    "vip_kdb_d800": "KDB-D800",
    "vip_cyd_luxury": "创宇盾豪华版",
    "vip_cyd_online": "创宇盾线上版",
    "vip_cyd_pro": "创宇盾旗舰版",
    "vip_cyd_signed": "创宇盾基础版",
    "vip_cyd_upper": "创宇盾高级版"
}


product_key = {
    "1": "CDN普通版",
    "2": "CDN政企版",
    "3": "抗D保旗舰版",
    "4": "抗D保豪华版",
    "5": "KDB-C10",
    "6": "KDB-C100",
    "7": "KDB-C5",
    "8": "KDB-C50",
    "9": "KDB-D10",
    "10": "KDB-D120",
    "11": "KDB-D20",
    "12": "KDB-D300",
    "13": "KDB-D50",
    "14": "KDB-D500",
    "15": "KDB-D80",
    "16": "KDB-D800",
    "17": "创宇盾豪华版",
    "18": "创宇盾线上版",
    "19": "创宇盾旗舰版",
    "20": "创宇盾基础版",
    "21": "创宇盾高级版"
}


exchange_trade_product_data = {v: k for k, v in trade_product_data.items()}


# print exchange_trade_product_data

def get_vip_trade_id(username, domain):
    vip_trade_id_url = "%s/service_manage/finance_details/list/?user=%s&domain=%s" % (api_url, username, domain)
    vip_trade_id_session = requests.session()
    vip_trade_id_session.headers = headers
    # __import__('pdb').set_trace()
    vip_trade_id_result = vip_trade_id_session.get(vip_trade_id_url).content
    vip_trade_id_guize = re.compile(r"trade_no=(.*)\"\>")
    return vip_trade_id_guize.findall(vip_trade_id_result)[0]


# print get_vip_trade_id("admin@knownsec.com","start-learn.win")

product = {
    "cdn": "",
    "waf": "",
    "ddos": "",
}


# cdn_list = [cdn for cdn in enumerate(trade_product_data.values(),0) if "CDN" in cdn]
# kdb_list = [kdb for kdb in trade_product_data.values() if "KDB" in kdb]
# waf_list = [waf for waf in trade_product_data.values() if "创宇盾" in waf]
# print cdn_list,kdb_list,waf_list


var_cdn_input = raw_input("输入CDN套餐: CDN普通版(1) | CDN政企版(2):")
var_kdb_input = raw_input("输入KDB套餐: 抗D保旗舰版(3) | 抗D保豪华版(4) | KDB-C10(5) | KDB-C100(6) | KDB-C5(7) | KDB-C50(8) | KDB-D10(9) | KDB-D120(10) | KDB-D20(11) | KDB-D300(12) | KDB-D50(13) | KDB-D500(14) | KDB-D80(15) | KDB-D800(16) :")
var_waf_input = raw_input("输入WAF套餐: 创宇盾豪华版(17) | 创宇盾线上版(18) | 创宇盾旗舰版(19) | 创宇盾基础版(20) | 创宇盾高级版(21) :")

# print var_cdn_input,var_kdb_input,var_waf_input
def input_product():

    try:
        if 1 <= int(var_cdn_input) <= 2:
            product['cdn'] = exchange_trade_product_data[product_key[var_cdn_input]]
            var_cdn = product_key[var_cdn_input]
    except:
        product['cdn'] = ""
        var_cdn=""

    try:
        if 3 <= int(var_kdb_input) <= 16:
            product['ddos'] = exchange_trade_product_data[product_key[var_kdb_input]]
            var_ddos = product_key[var_kdb_input]
    except:
        product['ddos'] = ""
        var_ddos = ""

    try:
        if 17 <= int(var_waf_input) <= 21:
            product['waf'] = exchange_trade_product_data[product_key[var_waf_input]]
            var_waf = product_key[var_waf_input]
    except:
        product['waf'] = ""
        var_waf = ""

    trade_product = "cdn:%s,ddos:%s,waf:%s" % (product['cdn'], product['ddos'], product['waf'])
    var_trade_product = "%s|%s|%s" % (var_cdn,  var_ddos, var_waf)
    return trade_product, var_trade_product

# vip_add_data['trade_product']=input_product()[0]
#
# print vip_add_data

def vip_add_requests(user_name, user_domain, expire_time, trade_number, trade_datatype, trade_money, vip_status, note):
    """
    :param user_name: 用户名
    :param user_domain: 根域名
    :param expire_time: 到期时间
    :param trade_number: 数量
    :param trade_datatype: 年月日
    :param trade_money: 金额
    :param vip_status: 套餐状态
    :param note: 备注信息
    :return:
    """
    # 当前时间 2016-12-29 23:15:22
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 转换成字符串时间
    time_array = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    # 转换成当前时间的时间戳
    time_stamp = time.mktime(time_array)
    # print now_time
    vip_add_url = "%s/service_manage/finance_details/vip_add/?timestamp=%s" % (api_url, time_stamp)
    # 保持 Cookie 会话
    vip_add_session = requests.session()
    vip_add_session.headers = headers
    # 用户名
    vip_add_data['trade_user'] = user_name
    # 根域名
    vip_add_data['trade_domain'] = user_domain
    # 数量
    vip_add_data['trade_amount'] = trade_number
    # 年月日
    vip_add_data['trade_unit'] = trade_datatype
    # 金额
    vip_add_data['trade_money'] = trade_money
    # 套餐类型
    vip_add_data['vip_status'] = vip_status
    vip_add_data['note'] = note
    vip_add_data['trade_product'] = input_product()[0]
    # 备注
    vip_add_result = vip_add_session.post(vip_add_url, data=vip_add_data).json()
    try:

        if "success" == vip_add_result['status']:
            vip_setting_data['trade_id'] = get_vip_trade_id(user_name, user_domain)
            vip_setting_data['expire_time'] = expire_time
            vip_setting_data['note'] = note
            vip_setting_data['trade_money'] = trade_money
            vip_setting_url = "%s/service_manage/finance_details/setting/?timestamp=%s" % (api_url, time_stamp)
            # 修改最近新加的套餐版本时间
            vip_setting_status = vip_add_session.post(vip_setting_url, data=vip_setting_data).json()
            if "success" == vip_setting_status['status']:
                # return vip_setting_status['message']
                return user_name, user_domain, input_product()[
                    1], expire_time, trade_number, trade_datatype, trade_money, vip_status, note

        elif "error" == vip_add_result['status']:
            return "套餐没开通成功,检查参数是否正确"
    except:
        return "疑似 cookies 失效，请检查"


def app_add_requests(flow_size, trade_money, trade_user, trade_domain, vip_status, note):
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_array = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = time.mktime(time_array)
    app_add_url = "%s/service_manage/finance_details/app_add/?timestamp=%s" % (api_url, time_stamp)
    app_session = requests.session()
    app_session.headers = headers
    # 流量大小单位是G
    app_add_data['trade_amount'] = flow_size
    # 金额
    app_add_data['trade_money'] = trade_money
    # if int(trade_money) >= 0:
    #     app_add_data['trade_money'] = trade_money
    # elif int(trade_money) == 0:
    #     app_add_data['trade_money'] = "0.0"
    # 用户名
    app_add_data['trade_user'] = trade_user
    # 域名
    app_add_data['trade_domain'] = trade_domain
    # 备注
    app_add_data['note'] = note
    # 套餐类型
    app_add_data['vip_status'] = vip_status
    app_add_result = app_session.post(app_add_url, data=app_add_data).json()
    return app_add_result['message'], now_time


def application_add(username, domain, expire_time, flowsize, amount, datetype, money, viptype, note):
    vip_add_requests(username, domain, expire_time, amount, datetype, money, viptype, note)
    app_add_requests(flowsize, money, username, domain, viptype, note)
    return username, domain, expire_time, flowsize, amount, datetype, money, viptype, note


vip_status = {
    "trial": "试用",
    "present": "赠送",
    "official": "正式",
    "month": "月",
    "day": "天",
    "year": "年"
}
# 字典键值对交换
exchange_vip_status = {v: k for k, v in vip_status.items()}

bandwidth_deduct_data = {
    'csrfmiddlewaretoken': 'In8SYk0F3Ob2Zj3RbFJNuLZBjEu8GMb7',
    'domain': 'start-learn.win',
    'username': 'admin@knownsec.com',
    'exceed': '1',
    'note': '111'
}


def get_domain_bandwidth(domain, username, note):
    domain_bandwidth_session = requests.session()
    domain_bandwidth_session.headers = headers
    domain_bandwidth_url = "%s/service_manage/service_status/list/?domain=%s&username=%s" % (api_url, domain, username)
    domain_bandwidth_result = domain_bandwidth_session.get(domain_bandwidth_url).content
    domain_bandwidth_guize = re.compile(r"<td>(.*)</td>")
    domain_bandwidth = int(
        re.sub("G", "", domain_bandwidth_guize.findall(domain_bandwidth_result)[10]).split(".")[0]) * 1024
    decut_bandwidth_url = "%s/domain_manage/bandwidth_deduct/add/" % api_url
    bandwidth_deduct_data['exceed'] = domain_bandwidth
    bandwidth_deduct_data['username'] = username
    bandwidth_deduct_data['domain'] = domain
    bandwidth_deduct_data['note'] = note
    bandwidth_deduct_data['csrfmiddlewaretoken'] = get_csrftoken()
    decut_bandwidth = domain_bandwidth_session.post(decut_bandwidth_url, data=bandwidth_deduct_data).json()
    # print domain_bandwidth
    if u"添加成功" in decut_bandwidth['message']:
        return domain_bandwidth, "流量清理完毕"
    else:
        return domain_bandwidth, "流量清理发生异常，请后台查询"
        # return domain_bandwidth, decut_bandwidth['message']


# print get_domain_bandwidth("163.com","admin@knownsec.com","测试清理流量")[1]

result = {
    "用户名": "",
    "根域名": "",
    "流量大小": "",
    "到期时间": "",
    "数量": "",
    "时间类型": "",
    "订单金额": "",
    "套餐状态": "",
    "剩余流量大小": "",
    "清理流量状态": "",
    "备注信息": ""
}


def official_add_vip(user_name, user_domain, flow_size, expire_time, trade_number, trade_datatype, trade_money,
                     vip_status, note):
    if "official" == exchange_vip_status[vip_status]:
        bandwidth_status = get_domain_bandwidth(user_domain, user_name, note)
        vip_add_requests(user_name, user_domain, expire_time, trade_number, exchange_vip_status[trade_datatype],
                         trade_money, exchange_vip_status[vip_status], note)
        app_add_requests(flow_size, trade_money, user_name, user_domain, exchange_vip_status[vip_status], note)
        # official_DATA = vip_add + app_add + bandwidth_status
        result['用户名'] = user_name
        result['根域名'] = user_domain
        result['套餐版本'] = input_product()[1]
        result['流量大小'] = flow_size
        result['到期时间'] = expire_time
        result['数量'] = trade_number
        result['时间类型'] = trade_datatype
        result['订单金额'] = trade_money
        result['套餐状态'] = vip_status
        result['备注信息'] = note
        result['剩余流量大小'] = bandwidth_status[0]
        result['清理流量状态'] = bandwidth_status[1]
        return result

    elif "trial" == exchange_vip_status[vip_status]:
        bandwidth_status = get_domain_bandwidth(user_domain, user_name, note)
        vip_add_requests(user_name, user_domain, expire_time, trade_number, exchange_vip_status[trade_datatype],
                         trade_money, exchange_vip_status[vip_status], note)
        app_add_requests(flow_size, trade_money, user_name, user_domain, exchange_vip_status[vip_status], note)
        # official_DATA = vip_add + app_add + bandwidth_status
        result['用户名'] = user_name
        result['根域名'] = user_domain
        result['套餐版本'] = input_product()[1]
        result['流量大小'] = flow_size
        result['到期时间'] = expire_time
        result['数量'] = trade_number
        result['时间类型'] = trade_datatype
        result['订单金额'] = trade_money
        result['套餐状态'] = vip_status
        result['备注信息'] = note
        result['剩余流量大小'] = bandwidth_status[0]
        result['清理流量状态'] = bandwidth_status[1]
        return result

    elif "present" == exchange_vip_status[vip_status]:
        # bandwidth_status = get_domain_bandwidth(user_domain,user_name,note)
        vip_add_requests(user_name, user_domain, expire_time, trade_number, exchange_vip_status[trade_datatype],
                         trade_money, exchange_vip_status[vip_status], note)
        app_add_requests(flow_size, trade_money, user_name, user_domain, exchange_vip_status[vip_status], note)
        # official_DATA = vip_add + app_add + bandwidth_status
        result['用户名'] = user_name
        result['根域名'] = user_domain
        result['套餐版本'] = input_product()[1]
        result['流量大小'] = flow_size
        result['到期时间'] = expire_time
        result['数量'] = trade_number
        result['时间类型'] = trade_datatype
        result['订单金额'] = trade_money
        result['套餐状态'] = vip_status
        result['备注信息'] = note
        result['剩余流量大小'] = "赠送版本以及流量无视"
        result['清理流量状态'] = "不清理了"
        return result


# print official_add_vip("admin@knownsec.com","163.com","7200","2017-12-31 15:32:45","1","年","0","正式","测试一下呢")


def online_add_vip(user_name, user_domain, flow_size, expire_time, trade_number, trade_datatype, trade_money,
                   vip_status, note):
    if "official" == exchange_vip_status[vip_status]:
        vip_add_requests(user_name, user_domain, expire_time, trade_number, exchange_vip_status[trade_datatype],
                         trade_money, exchange_vip_status[vip_status], note)
        app_add_requests(flow_size, trade_money, user_name, user_domain, exchange_vip_status[vip_status], note)
        result['用户名'] = user_name
        result['根域名'] = user_domain
        result['套餐版本'] = input_product()[1]
        result['流量大小'] = flow_size
        result['到期时间'] = expire_time
        result['数量'] = trade_number
        result['时间类型'] = trade_datatype
        result['订单金额'] = trade_money
        result['套餐状态'] = vip_status
        result['备注信息'] = note
        result['剩余流量大小'] = "线上客户流量累加"
        result['清理流量状态'] = "并不清理"
        return result

    elif "trial" == exchange_vip_status[vip_status]:
        vip_add_requests(user_name, user_domain, expire_time, trade_number, exchange_vip_status[trade_datatype],
                         trade_money, exchange_vip_status[vip_status], note)
        app_add_requests(flow_size, trade_money, user_name, user_domain, exchange_vip_status[vip_status], note)
        result['用户名'] = user_name
        result['根域名'] = user_domain
        result['套餐版本'] = input_product()[1]
        result['流量大小'] = flow_size
        result['到期时间'] = expire_time
        result['数量'] = trade_number
        result['时间类型'] = trade_datatype
        result['订单金额'] = trade_money
        result['套餐状态'] = vip_status
        result['备注信息'] = note
        result['剩余流量大小'] = "线上客户流量累加"
        result['清理流量状态'] = "并不清理"
        return result

    elif "present" == exchange_vip_status[vip_status]:
        vip_add_requests(user_name, user_domain, expire_time, trade_number, exchange_vip_status[trade_datatype],
                         trade_money, exchange_vip_status[vip_status], note)
        app_add_requests(flow_size, trade_money, user_name, user_domain, exchange_vip_status[vip_status], note)
        result['用户名'] = user_name
        result['根域名'] = user_domain
        result['套餐版本'] = input_product()[1]
        result['流量大小'] = flow_size
        result['到期时间'] = expire_time
        result['数量'] = trade_number
        result['时间类型'] = trade_datatype
        result['订单金额'] = trade_money
        result['套餐状态'] = vip_status
        result['备注信息'] = note
        result['剩余流量大小'] = "赠送版本以及流量无视"
        result['清理流量状态'] = "不清理了"
        return result


def batch_add():
    table = PrettyTable(["用户名", "根域名", "套餐版本", "到期时间","流量大小(G)", "数量", "日期类型", "金额", "套餐状态", "备注信息"])
    with open(vip_csv_path) as domain_information:
        reader_info = csv.DictReader(domain_information)
        for row in reader_info:
            get_domain_bandwidth(row['domain'], row['user_name'], row['note'])
            app = application_add(row['user_name'],row['domain'],  row['expire_time'],row['flow_size'], row['trade_number'],
                                  exchange_vip_status[row['trade_datatype']], row['trade_money'], exchange_vip_status[row['vip_status']],
                                  row['note'])
           # application_add()
            table.add_row([app[0], app[1], input_product()[1], app[2], app[3], app[4], vip_status[app[5]], app[6],
                           vip_status[app[7]], app[8]])
            # print app
    print table


def online_batch_add():
    table = PrettyTable(["用户名", "根域名", "套餐版本","到期时间", "流量大小(G)", "数量", "日期类型", "金额", "套餐状态", "备注信息"])
    with codecs.open(vip_csv_path) as domain_information:
        reader_info = csv.DictReader(domain_information)
        for row in reader_info:
            app = application_add(row['user_name'],row['domain'], row['expire_time'],row['flow_size'], row['trade_number'],
                                  exchange_vip_status[row['trade_datatype']], row['trade_money'], exchange_vip_status[row['vip_status']],
                                  row['note'])
            table.add_row([app[0], app[1], input_product()[1], app[2], app[3], app[4], vip_status[app[5]], app[6],
                           vip_status[app[7]], app[8]])
            # print app
    print table


def app_clean():
    table = PrettyTable(["用户名", "清理流量大小", "清理流量状态", "根域名", "备注信息"])
    with codecs.open(app_csv_path) as domain_information:
        reader_info = csv.DictReader(domain_information)
        for row in reader_info:
            clean = get_domain_bandwidth(row['根域名'], row['用户名'], row['备注信息'])
            table.add_row([row['根域名'], clean[0], clean[1], row['用户名'], row['备注信息']])
    print table


if __name__ == '__main__':
    if len(sys.argv[1:]) == 0:
        print "请输入参数"

    elif "-t" in sys.argv[1] or "--type" in sys.argv[1]:
        if "online" in sys.argv[2]:
            if "-m" in sys.argv[3] or "--mode" in sys.argv[3]:
                if sys.argv[4] == "solo":
                    print "线上单独加"
                    online_add_vip = online_add_vip(sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9],
                                                    sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13])
                    table = PrettyTable(
                        ["根域名", "用户名", "套餐版本", "流量大小", "到期时间", "数量", "时间类型", "订单金额", "套餐状态", "剩余流量大小", "清理流量状态",
                         "备注信息"])
                    table.add_row(
                        [result['根域名'], result['用户名'], result['套餐版本'], result['流量大小'], result['到期时间'], result['数量'],
                         result['时间类型'], result['订单金额'], result['套餐状态'], result['剩余流量大小'], result['清理流量状态'],
                         result['备注信息']])
                    print table
                elif sys.argv[4] == "batch":
                    online_batch_add()
                    print "线上批量加"
                else:
                    print "参数有问题"
            else:
                print "参数有误"

        elif "offline" in sys.argv[2]:
            if "-m" in sys.argv[3] or "--mode" in sys.argv[3]:
                if sys.argv[4] == "solo":
                    print "线下客户单独加"
                    official_add = official_add_vip(sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9],
                                                    sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13])
                    table = PrettyTable(
                        ["根域名", "用户名", "套餐版本", "流量大小", "到期时间", "数量", "时间类型", "订单金额", "套餐状态", "剩余流量大小", "清理流量状态",
                         "备注信息"])
                    table.add_row(
                        [result['根域名'], result['用户名'], result['套餐版本'], result['流量大小'], result['到期时间'], result['数量'],
                         result['时间类型'], result['订单金额'], result['套餐状态'], result['剩余流量大小'], result['清理流量状态'],
                         result['备注信息']])
                    print table
                elif sys.argv[4] == "batch":
                    print "线下批量加"
                    batch_add()
                else:
                    print "参数有问题"
            else:
                print " 参数有问题"
        elif "clear" in sys.argv[2]:
            app_clean()
