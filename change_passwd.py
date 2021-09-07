# -*- coding: utf-8 -*-
__author__ = 'suxiaojin'
__date__ = '2021/8/2 0002 下午 14:51'

import paramiko


def change_passwd():
    p_file = open('passwd.txt', 'r')
    for l in p_file:
        inform = l.split()
        ip = inform[0]
        username = inform[1]
        old_passwd = inform[2]
        new_passwd = inform[3]
        port = inform[4]
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(hostname=ip, port=int(port), username=username, password=old_passwd)
            print('"%s" is updating password' % ip)
            stdin, stdout, stderr = ssh.exec_command('echo %s |passwd --stdin %s' % (new_passwd, username))
            result = str(stdout.read())
            if "successfully" in result:
                print('%s change password is ok!' % ip)
            else:
                print('%s change password is failed!' % ip)
            ssh.close()
        except Exception as e:
            print(e)
            print("connection error")


if __name__ == '__main__':
    change_passwd()
