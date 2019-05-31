#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getSystemVersion.py
User:               Guodong
Create Date:        2016/12/16
Create Time:        14:51
 """
import os
import platform
import subprocess
import sys

import time

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
linux = (sys.platform == "linux2")

hidden_hostname = False

if mswindows:
    uname = list(platform.uname())
    if hidden_hostname:
        uname[1] = "hidden_hostname"
    print(tuple(uname))

    import winreg

    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")
        if reg_key:
            InstallationType = winreg.QueryValueEx(reg_key, "InstallationType")[0] or ""
            if InstallationType and InstallationType == 'Client':
                InstallDate = time.strftime('%Y-%m-%d %H:%M:%S',
                                            time.localtime(winreg.QueryValueEx(reg_key, "InstallDate")[0]))
                ProductName = winreg.QueryValueEx(reg_key, "ProductName")[0] or None
                EditionId = winreg.QueryValueEx(reg_key, "EditionId")[0] or None
                ReleaseId = winreg.QueryValueEx(reg_key, "ReleaseId")[0] or None
                CurrentBuild = winreg.QueryValueEx(reg_key, "CurrentBuild")[0] or None
                CurrentVersion = winreg.QueryValueEx(reg_key, "CurrentVersion")[0] or None
                BuildLabEx = winreg.QueryValueEx(reg_key, "BuildLabEx")[0][:9] or None
                ProductId = winreg.QueryValueEx(reg_key, "ProductId")[0] or None
                print((
                    InstallDate, ProductName, EditionId, ReleaseId, CurrentVersion, CurrentBuild, BuildLabEx,
                    ProductId))
            elif InstallationType and InstallationType == 'Server':
                InstallDate = time.strftime('%Y-%m-%d %H:%M:%S',
                                            time.localtime(winreg.QueryValueEx(reg_key, "InstallDate")[0]))
                ProductName = winreg.QueryValueEx(reg_key, "ProductName")[0] or None
                EditionId = winreg.QueryValueEx(reg_key, "EditionId")[0] or None
                CurrentVersion = winreg.QueryValueEx(reg_key, "CurrentVersion")[0] or None
                CurrentBuild = winreg.QueryValueEx(reg_key, "CurrentBuild")[0] or None
                BuildLabEx = winreg.QueryValueEx(reg_key, "BuildLabEx")[0][:9] or None
                if CurrentVersion <= '6.1':  # 6.1 include 'Windows Server 2008 R2(6.1)'
                    print((InstallDate, ProductName, EditionId, CurrentVersion, CurrentBuild, BuildLabEx))
                else:
                    ProductId = winreg.QueryValueEx(reg_key, "ProductId")[
                                    0] or None  # Windows Server 2008 R2 is not supported
                    print((InstallDate, ProductName, EditionId, CurrentVersion, CurrentBuild, BuildLabEx, ProductId))
    except WindowsError as e:
        print('WindowsError is captured.')
        print(e)
        print(e.args)
    except Exception as e:
        print(e)
        print(e.args)

if linux:
    uname = list(platform.uname())
    if hidden_hostname:
        uname[1] = "hidden_hostname"
    print(uname)

    proc_obj = subprocess.Popen(r'uname -a', shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    result = proc_obj.stdout.read().strip()
    if result:
        print(result)

    if os.path.isfile("/proc/version"):
        with open("/proc/version", 'r') as f:
            content = f.read().strip()
        if content != "":
            print(content)

    if os.path.isfile("/etc/issue"):
        with open("/etc/issue", 'r') as f:
            content = f.read().strip()
        if content != "":
            print(content)
