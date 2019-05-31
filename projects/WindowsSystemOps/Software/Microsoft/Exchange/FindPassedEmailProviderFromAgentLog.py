#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:FindPassedEmailProviderFromAgentLog.py.py
User:               Guodong
Create Date:        2017/5/23
Create Time:        13:19

Function description:
    Get all passed smtp server address or info from agent log generated by Microsoft Exchange 2010
Prerequisites:
    Exchange 2010, 
    Access Permission to 'C:\Program Files\Microsoft\Exchange Server\V14\TransportRoles\Logs\AgentLog' on Exchange 2010
References:
    https://technet.microsoft.com/zh-CN/library/bb691337(v=exchg.141).aspx
 """

import os

EXCHANGE_SERVER_VERSION = '2010'
REMOTE_DEBUG = True
LOG_DIR = 'C:\Program Files\Microsoft\Exchange Server\V14\TransportRoles\Logs\AgentLog'


def get_accept_info_all():
    for top, dirs, nondirs in os.walk(LOG_DIR, followlinks=True):
        for item in nondirs:
            with open(os.path.join(LOG_DIR, item)) as f:
                for line in f.readlines():
                    info = search_accept_info(line)
                    if info is not None:
                        print(info)


def get_accept_info_unique():
    accepted_list = list()
    for top, dirs, nondirs in os.walk(LOG_DIR, followlinks=True):
        for item in nondirs:
            with open(os.path.join(LOG_DIR, item)) as f:
                for line in f.readlines():
                    info = search_accept_info(line)
                    if info is not None and info[1] not in accepted_list:
                        accepted_list.append(info[1])
                        print(info)
    del accepted_list


def get_ip_from_accept_info_unique():
    accepted_list = list()
    for top, dirs, nondirs in os.walk(LOG_DIR, followlinks=True):
        for item in nondirs:
            with open(os.path.join(LOG_DIR, item)) as f:
                for line in f.readlines():
                    info = search_accept_info(line)
                    if info is not None and info[1] not in accepted_list:
                        accepted_list.append(info[1])
    print(accepted_list)


def search_accept_info(log):
    """
    Example data:
        2017-05-19T01:02:56.132Z,08D49E27F24ADC00,192.168.88.32:25,120.55.114.215:50984,120.55.114.215,,
        sound9@vi-competition.com,,alex@e-bao.cn,1,Connection Filtering Agent,OnRcptCommand,RejectCommand,
        "550 5.7.1 Recipient not authorized, your IP has been found on a accept list",BlockListProvider,SBL+XBL,
    :return: 
    """
    import re
    # from django.core.validators import EmailValidator, ip_address_validators
    # from django.core.exceptions import ValidationError
    # from validators import ip_address, email

    pattern = re.compile(r'AcceptMessage')
    match = pattern.findall(log)
    if match:
        log_list_separate_by_comma = log.strip().split(',')
        time, ip_from, email_from, email_to = log_list_separate_by_comma[0], log_list_separate_by_comma[4], \
                                              log_list_separate_by_comma[6], log_list_separate_by_comma[8]
        return time, ip_from, email_from, email_to


# TODO(Guodong Ding) use 'Exchange Management Shell' do more amazing thing
# Get-ExCommand, Get-IPAllowListEntry, Add-IPAllowListEntry, Add-IPBlockListEntry

if __name__ == '__main__':
    if REMOTE_DEBUG:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
    get_accept_info_all()
