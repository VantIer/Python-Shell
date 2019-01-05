#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Connect to Target'

__author__ = 'Vantler'

# 导入socket库:
import socket
import time

# 变量定义
IP = '127.0.0.1'
PORT = 9481
PASS = 'AC131'

#文字颜色
# 红色 \033[0;31;48m[!]\033[0m
# 绿色 \033[0;32;48m[+]\033[0m
# 黄色 \033[0;33;48m[-]\033[0m
# 蓝色 \033[0;36;48m[*]\033[0m

# 获取目标地址:
def Target():
    global IP,PORT,PASS
    Input = input('>>> Target IP/Host (now: %s): ' %IP)
    if Input:
        IP = Input
    print('\033[0;32;48m[+]\033[0mYour Target IP/Host is \033[0;36;48m%s\033[0m\n' %IP)
    while True:
        Input = input('>>> PORT (now: %d): ' %PORT)
        if not Input:
            print('\033[0;32;48m[+]\033[0mYour Target Port is \033[0;36;48m%d\033[0m\n' %PORT)
            break
        if Input.isdecimal():
            Input = int(Input)
            if Input >=1 and Input <= 65535:
                PORT = Input
                Input = None
                print('\033[0;32;48m[+]\033[0mYour Target Port is \033[0;36;48m%d\033[0m\n' %PORT)
                break
        print('\n\033[0;31;48m[!]\033[0mERROR: Please input a VALID port.\n')
    Input = input('>>> Password (now: %s): ' %PASS)
    if Input:
        PASS = Input
    print('\033[0;32;48m[+]\033[0mYour Password is \033[0;36;48m%s\033[0m\n' %PASS)
    return

# 创建连接
def Connect():
    while True:
        Target()
        print('\033[0;36;48m[*]\033[0mConnecting to target ...')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if s.connect_ex((IP, PORT)) != 0:
            print('\033[0;31;48m[!]\033[0mERROR: Connection Failed.\n')
            s.close()
        elif TargetCheck(s):
            return s
        else:
            s.close()

# 监听连接
def Listen():
    global PORT
    while True:
        Input = input('>>> Listening PORT (now: %d): ' %PORT)
        if not Input:
            print('\033[0;32;48m[+]\033[0mYour Listening Port is \033[0;36;48m%d\033[0m\n' %PORT)
            break
        if Input.isdecimal():
            Input = int(Input)
            if Input >=1 and Input <= 65535:
                PORT = Input
                Input = None
                print('\033[0;32;48m[+]\033[0mYour Listening Port is \033[0;36;48m%d\033[0m\n' %PORT)
                break
        print('\n\033[0;31;48m[!]\033[0mERROR: Please input a VALID port.\n')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0',PORT))
    s.listen(1)
    print('\033[0;36;48m[*]\033[0mListening for connections ...')
    while True:
        sock, addr = s.accept()
        if TargetCheck(sock):
            print('\n\033[0;32;48m[+]\033[0mTarget \033[0;33;48m%s\033[0m : %s login.\n' % addr)
            return sock

# 目标有效性检查
def TargetCheck(s):
    password = PASS.encode('ascii')
    s.send(b'Vshell P%s' %password)
    d = s.recv(1024)
    data = d.decode('utf-8')
    if data:
        if data == 'HiAdmin':
            return True
        elif data == 'NoAccess':
            print('\033[0;33;48m[-]\033[0mWrong Password.\n')
            return False
        else:
            print('\033[0;31;48m[!]\033[0mWrong Target.\n')
            return False
    else:
        print('\033[0;31;48m[!]\033[0mNo Response.\n')
        return False

if __name__=='__main__':
    print('\nI think you should try \033[0;32;48mMAIN.PY\033[0m.    ㄟ( ▔, ▔ )ㄏ\n')