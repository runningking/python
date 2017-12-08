#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/9/19 下午5:16
# @Author  : wubin
# @Site    : https://www.cnhzz.com
# @File    : ptyy_mail.py
# @Software: PyCharm


import requests

post_url = "http://api.sendcloud.net/apiv2/mail/sendtemplate"

post_data = {
    "apiUser": "pl_ptyy",
    # "apiUser": "ptyy_pl", # mail.365cyd.com
    # "apiKey": "A7ZaS2nK5E263dCi",
    "apiKey": "SZmBpyK6zrB2Enuj",     # jiasule.com
    # "apiKey": "3GaQnZK72fOR43ZP",       # mail.365cyd.com
    'useAddressList': "true",
    "from": "kefu@jiasule.com",
    "fromName": "知道创宇云安全<kefu@jiasule.com>",
    "subject": "【知道创宇云安全】云主机白名单添加",
    "replyTo": "kefu@jiasule.com",
    # 发送邮件的模板
    "templateInvokeName": "HX_yunzhuji",
    "contentSummary":"",
    # "to": "diaocha3w@maillist.sendcloud.org",
    "to": "HX_yunzhuji@maillist.sendcloud.org",
}


task_info_data = {

    "apiUser": "pl_ptyy",
    "apiKey": "SZmBpyK6zrB2Enuj",
    "maillistTaskId": "432913"

}


# 获取发送状态
def task_info():
    # taskinfo_data["maillistTaskId"] = r['info']['maillistTaskId']
    r_task_info = requests.post("http://api.sendcloud.net/apiv2/mail/taskinfo", data=task_info_data)
    print(r_task_info.json()['message'], r_task_info.json()['info']['data']['status'],
          r_task_info.json()['info']['data'][
              'memberCount'])


addressmember = {

    "apiUser": "pl_ptyy",
    "apiKey": "SZmBpyK6zrB2Enuj",
    "address": "2015-2016@maillist.sendcloud.org",
    "members": "admin@cnhzz.com",
    "vars": '{"username":"admin@cnhzz.com"}',

}

def add_user_mail():
    f = open("/Users/wubin/Desktop/mail.txt")
    for domain in f.readlines():
        addressmember['members'] = domain.split()[0]
        addressmember['vars'] = "{'username':'%s'} " % domain.split()[0]
        # print addressmember
        user_add_url = "http://api.sendcloud.net/apiv2/addressmember/add"
        r_user_add_url = requests.post(user_add_url, data=addressmember).json()
        print(r_user_add_url['message'], r_user_add_url['info']['count'])


# 添加邮件地址以及用户名
# add_user_mail()

# f = open("/Users/nibuw/Desktop/mail.txt")
# for user_mail in f.readlines():
#     try:
#         user = "<%s>,{'username':'%s'}" % (user_mail.split()[0], user_mail.split()[0])
#         print user
#     except:
#         print user_mail
#     # print(user)


# 发送邮件
if __name__ == '__main__':
    r = requests.post(post_url, data=post_data).json()
    result = "%s,%s,%s" % (r['message'], r['info']['maillistTaskId'], r['message'])
    print(result)
