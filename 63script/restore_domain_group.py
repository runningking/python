#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/6/27 10:24
# @Author : 吴彬-bingoku
# @Site : https://www.cnhzz.com
# @File : restore_domain_group.py
# @Software: PyCharm


import subprocess
import commands

"for domain_id in `chgroup.py -g $1 --list | awk '{print $1}'`;do chgroup.py -i $domain_id -g $2;done"


def get_domain_id(gid):

    get_domain_id_cmd = "python chgroup.py -g %s --list | awk '{print $1}'" % gid
    domain_id = subprocess.check_output(get_domain_id_cmd, shell=True).split()
    return domain_id

class Move_group_domain():

    def chgroup_group_domain(self,source_gid, target_gid):
        chgroup_domain_list = []
        old_gid_domain_id = get_domain_id(source_gid)
        for read_domain_id in old_gid_domain_id:
            chgroup_domain_id_cmd = "python chgroup.py -i %s -g %s | awk '{print $2}' | awk -F ')' '{print $1}'" % (read_domain_id, target_gid)
            chgroup_domain = commands.getoutput(chgroup_domain_id_cmd).split()
            chgroup_domain_list.append(chgroup_domain[0])
        return chgroup_domain_list





print Move_group_domain.chgroup_group_domain(source_gid=60,target_gid=60)
