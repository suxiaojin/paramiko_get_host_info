# -*- coding: utf-8 -*-
__author__ = 'suxiaojin'
__date__ = '2021/8/27 0027 上午 10:34'

'''
如果远程服务器连接不上，直接返回
登陆到远程服务器之后sudo -i 切换到root , 2个操作：1、解锁 pam_tally2 -r -u zxadmin  2、改密码 pam_tally2 -r -u zxadmin 
                                    passwd zxadmin  初始密码是1qaz@WSX
'''
import paramiko


def unlock_change_passwd():
    p_file = open('unlock_change_pwd.txt', 'r')
    for l in p_file:
        inform = l.split()
        ip = inform[0]
        username = inform[1]
        pwd = inform[2]
        menus = {
            'a': '解锁',
            'b': '改密码',
            'q': '退出',
        }
        print(menus)
        while True:
            cmd = input('请输入:')
            if cmd == 'a':
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                    ssh.connect(hostname=ip, port=22, username=username, password=pwd)
                    print('"%s" 连接成功' % ip)
                    stdin, stdout, stderr = ssh.exec_command('sudo pam_tally2 -r -u zxadmin')
                    print(stdout.read())
                    ssh.close()
                except Exception as e:
                    print(e)
                    print("connection error")
            if cmd == 'b':
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                    ssh.connect(hostname=ip, port=22, username=username, password=pwd)
                    print('"%s" 连接成功' % ip)
                    stdin, stdout, stderr = ssh.exec_command(
                        'sudo pam_tally2 -r -u zxadmin;sudo -i; echo 2qaz@WSX |passwd --stdin zxadmin', get_pty=True)
                    result = str(stdout.read())
                    if "successfully" in result:
                        print('%s change password is ok!' % ip)
                    else:
                        print('%s change password is failed!' % ip)
                    ssh.close()
                except Exception as e:
                    print(e)
                    print("connection error")
            if cmd == 'q':
                break


if __name__ == '__main__':
    unlock_change_passwd()
