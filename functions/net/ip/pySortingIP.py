#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySortingIP.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/6
Create Time:            15:30
Description:            allow internal network to connect
Long Description:       
References:             https://stackoverflow.com/questions/13853493/sort-list-of-ip-addresses-with-subnet-mask
Prerequisites:          []
                        yum install python-devel
                        pip3 install --upgrade pip
                        pip3 install netifaces
                        pip3 install ipcalc
                        pip3 install IPy
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import ipcalc
from IPy import IP


# gateways_dict = netifaces.gateways()
# gateways_json = json.dumps(gateways_dict, indent=5)
# print gateways_json

def is_valid_ipv4(ip, version=4):
    try:
        result = IP(ip, ipversion=version)
    except ValueError:
        return False
    if result is not None and result != "":
        return True


def is_private_ipv4(ip, version=4):
    if is_valid_ipv4(ip, version):
        if not ip.startswith('0.0.0.0') and (IP(ip).iptype() == "PRIVATE" or IP(ip).iptype() != "PUBLIC"):
            return True
        else:
            return False
    else:
        raise RuntimeError("Error: invalid ip address: %s" % ip)


# route -n | sed '1,2d' | awk -F'[ ]+' '{print $1 "/" $3}'
route = """
121.199.12.0/255.255.252.0
10.132.0.0/255.255.240.0
169.254.0.0/255.255.0.0
169.254.0.0/255.255.0.0
172.16.0.0/255.240.0.0
100.64.0.0/255.192.0.0
10.0.0.0/255.0.0.0
0.0.0.0/0.0.0.0
"""

net_connected = list()
for line in set(route.strip().split('\n')):
    if is_private_ipv4(line):
        net_connected.append(ipcalc.Network(line).__str__())


def key_sort_ip(addr):
    # https://stackoverflow.com/questions/13853493/sort-list-of-ip-addresses-with-subnet-mask
    add, pref = addr.split("/")
    a, b, c, d = (int(x) for x in add.split("."))
    return a, b, c, d, int(pref)


net_connected_sorted = sorted(net_connected, key=key_sort_ip)  # sorting IP address

for item in net_connected_sorted:
    print(item)
