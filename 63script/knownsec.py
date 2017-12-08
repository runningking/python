#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/22 上午10:16
# @Author  : wubin
# @Site    : https://www.cnhzz.com
# @File    : knownsec.py
# @Software: PyCharm

import urllib2
import urllib
import json
import re

url = "http://10.8.2.10/ac_portal/login.php"
data = {
    'opr': 'pwdLogin',
    'userName': 'ks00071',
    'pwd': 'maybe21c@163.com',
    'rememberPwd': '1'
}
if __name__ == '__main__':
    format_data = urllib.urlencode(data)
    req = urllib2.Request(url,format_data)
    html = urllib2.urlopen(req,timeout=5).read()
    result = html.replace("false", "'false'").replace("true", "'true'").replace(":0", ":'0'")
    result_json = json.loads(re.sub("\'", "\"", result))
    print result_json["msg"]


    # r = requests.post(url, data=data, stream=True).content
    # result = r.decode("utf-8").replace("false", "'false'").replace("true", "'true'").replace(":0", ":'0'")
    # result_json = json.loads(re.sub("\'", "\"", result))
    # print(result_json["msg"])

