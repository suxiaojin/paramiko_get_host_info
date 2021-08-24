# -*- coding: utf-8 -*-
__author__ = 'suxiaojin'
__date__ = '2021/7/29 0029 下午 14:04'

import os, sys
import paramiko
import xlsxwriter
import time


def sshcmd(ip, port, username, pwd):
    tmplist = {"ip": ip, "cpuuse": None, "memoryall": None, "memoryuse": None, "diskall": None, "diskuse": None,
               "homeall": None, "homeuse": None}
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=ip, port=port, username=username, password=pwd)
        stdincpu, stdoutcpu, stderrcpu = ssh.exec_command(
            "top -b -n 1|head -n 4|grep 'Cpu(s)'|awk '{print $2}'|cut -d 'u' -f 1")
        stdinmemoryall, stdoutmemoryall, stderrmemoryall = ssh.exec_command(
            "free -m | awk '{print $2}' | awk 'NR==2{print}'")
        stdinmemory, stdoutmemory, stderrmemory = ssh.exec_command(
            "echo `free -m | sed -n '2p' | awk '{print  ($2-$7)/$2*100}'|awk -F'.' '{print $1}'`%")
        stdindiskall, stdoutdiskall, stderrdiskall = ssh.exec_command("df -hP | awk '/\/$/ {print $2}'")
        stdindisk, stdoutdisk, stderrdisk = ssh.exec_command("df -hP | awk '/\/$/ {print $5}'")
        stdinhomeall, stdouthomeall, stderrhomeall = ssh.exec_command(
            "df -hP /home | awk '{print $2}' | awk 'NR==2{print}'")
        stdinhome, stdouthome, stderrhome = ssh.exec_command("df -hP /home | awk '{print $5}' |awk 'NR==2{print}'")

        tmplist["ip"] = ip
        tmplist["cpuuse"] = (stdoutcpu.read()).decode()
        tmplist["memoryall"] = (stdoutmemoryall.read()).decode()
        tmplist["memoryuse"] = (stdoutmemory.read()).decode()
        tmplist["diskall"] = (stdoutdiskall).read().decode()
        tmplist["diskuse"] = (stdoutdisk.read()).decode()
        tmplist["homeall"] = (stdouthomeall).read().decode()
        tmplist["homeuse"] = (stdouthome).read().decode()
        print(tmplist)
        return tmplist
        ssh.close()
    except Exception as e:
        print(e)
        return tmplist


def trywexrestr(lists):
    nowtime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + ""
    bookurl = "systems" + nowtime + 'info.xlsx'
    # filenames=nowtime+'info.xlsx'
    workbook1 = xlsxwriter.Workbook(bookurl)
    worksheet = workbook1.add_worksheet()
    title = [u'IP地址', u'CPU使用率', u'内存总量', u'内存使用率', u'根目录大小', u'根目录使用百分比', u'home大小' \
        , u'home使用率']
    format = workbook1.add_format()
    worksheet.set_column(0, 15, 20)
    format.set_bold()
    worksheet.write_row('A1', title, format)
    row = 1

    for a in lists:
        worksheet.write(row, 0, a["ip"])
        worksheet.write(row, 1, a["cpuuse"])
        worksheet.write(row, 2, a["memoryall"])
        worksheet.write(row, 3, a["memoryuse"])
        worksheet.write(row, 4, a["diskall"])
        worksheet.write(row, 5, a["diskuse"])
        worksheet.write(row, 6, a["homeall"])
        worksheet.write(row, 7, a["homeuse"])
        row = row + 1
    workbook1.close()


def readinfo():
    f = open('ip.txt', 'r')
    listall = []
    for line in f.readlines():
        ip, port, username, pwd = line.split()
        tmplist = sshcmd(ip, int(port), username, pwd)
        listall.append(tmplist)
    return listall


listall = readinfo()
trywexrestr(listall)
