#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入socket库:
import socket
import connect
import time

# 变量定义 ACTIVE 是否主动连接被控端
ACTIVE = 1

#文字颜色
# 红色 \033[0;31;48m[!]\033[0m
# 绿色 \033[0;32;48m[+]\033[0m
# 黄色 \033[0;33;48m[-]\033[0m
# 蓝色 \033[0;36;48m[*]\033[0m

# 功能列表
def Functions():
    print('\033[0;32;48m[+]\033[0m Functions:')
    print('[1] Information')
    print('[2] Process Management')
    print('[3] File Management')
    print('[0] Exit\n')

# 系统信息
def Information(sock):
    sock.send(b'1')
    buffer = []
    while True:
        d = sock.recv(1024)
        if d != b'End':
            buffer.append(d)
        else:
            break
    data = b''.join(buffer)
    data = data.decode('utf-8')
    info = data.split('@',1)
    print('\n%s\n' % info[1])
    if info[0] == 'nt':
        return
    else:
        while True:
            print('\033[0;32;48m[+]\033[0m More Info:')
            print('[1] CPU Info')
            print('[2] Mem Info')
            print('[3] USB Info')
            print('[0] Exit\n')
            if Linuxinfo(sock):
                break
        return

# Linux系统信息
def Linuxinfo(sock):
    while True:
        Input = input('>>> Information ID: ')
        if not Input:
            print('\033[0;33;48m[-]\033[0mYou must choose one function.\n')
        elif Input.isdecimal():
            Input = int(Input)
            if Input == 0:
                return True
            elif Input == 1 or Input == 2 or Input == 3:
                if Input == 1:
                    sock.send(b'1x01')
                elif Input == 2:
                    sock.send(b'1x02')
                elif Input == 3:
                    sock.send(b'1x03')
                buffer = []
                while True:
                    d = sock.recv(1024)
                    if d != b'End':
                        buffer.append(d)
                    else:
                        break
                data = b''.join(buffer)
                data = data.decode('utf-8')
                print('\n%s\n' % data)
                return False
            else:
                print('\033[0;33;48m[-]\033[0mWrong ID. Please choose another one (? to get list).\n')
        else:
            print('\033[0;33;48m[-]\033[0mWrong Input.You must choose a correct function (? to get list).\n')

# 进程管理
def Process(sock):
    sock.send(b'2')
    buffer = []
    while True:
        d = sock.recv(1024)
        if d != b'End':
            buffer.append(d)
        else:
            break
    data = b''.join(buffer)
    data = data.decode('utf-8')
    print('\n%s\n' % data)
    while True:
        print('\033[0;32;48m[+]\033[0m More Info:')
        print('[1] Kill by Name (Only for Win)')
        print('[2] Kill by ID')
        print('[3] Process List')
        print('[0] Exit\n')
        if Processmanage(sock):
            break
    return

# 进程操作
def Processmanage(sock):
    while True:
        Input = input('>>> Order ID: ')
        if not Input:
            print('\033[0;33;48m[-]\033[0mYou must choose one function.\n')
        elif Input.isdecimal():
            Input = int(Input)
            if Input == 0:
                return True
            elif Input == 1 or Input == 2 or Input == 3:
                if Input == 1:
                    sock.send(b'2x01')
                    Input = input('>>> Process Name: ')
                    Input = Input.encode('utf-8')
                    sock.send(Input)
                elif Input == 2:
                    sock.send(b'2x02')
                    Input = input('>>> Process ID: ')
                    Input = Input.encode('utf-8')
                    sock.send(Input)
                elif Input == 3:
                    sock.send(b'2')
                    buffer = []
                    while True:
                        d = sock.recv(1024)
                        if d != b'End':
                            buffer.append(d)
                        else:
                            break
                    data = b''.join(buffer)
                    data = data.decode('utf-8')
                    print('\n%s\n' % data)
                    return False
                d = sock.recv(1024)
                data = d.decode('utf-8')
                print('\n%s\n' % data)
                return False
            else:
                print('\033[0;33;48m[-]\033[0mWrong ID. Please choose another one (? to get list).\n')
        else:
            print('\033[0;33;48m[-]\033[0mWrong Input.You must choose a correct function (? to get list).\n')

# 主程序
print('\n\n')
print('          \033[0;33;48m\\\\\033[0m  \033[0;34;48mPython\033[0m   \033[0;31;48m//\033[0m')
print('           \033[0;33;48m\\\\\033[0m  \033[0;32;48mShell\033[0m  \033[0;31;48m//\033[0m')
print('            \033[0;33;48m\\\\\033[0m       \033[0;31;48m//\033[0m')
print('             \033[0;33;48m\\\\\033[0m     \033[0;31;48m//\033[0m')
print('              \033[0;33;48m\\\\\033[0m   \033[0;31;48m//\033[0m')
print('               \033[0;33;48m\\\\\033[0m \033[0;31;48m//\033[0m')
print('                \033[0;33;48m\\\033[0m\033[0;36;48mV\033[0m\033[0;31;48m/\033[0m')
print('\n\n')

# 创建连接
while True:
    Input = input('>>> Active Connect? (Y/N) : ')
    Input = Input.upper()
    if Input == 'Y':
        print('\033[0;32;48m[+]\033[0mActive Mode\n')
        ACTIVE = 1
        break
    elif Input == 'N':
        print('\033[0;32;48m[+]\033[0mPassive Mode\n')
        ACTIVE = 0
        break
    else:
        print('\033[0;33;48m[-]\033[0mYou should choose a way to connect Target.\n')
if ACTIVE == 1:
    s = connect.Connect()
else:
    s = connect.Listen()
# 功能部分
Functions()
while True:
    Input = input('>>> Function ID (? to get list): ')
    if not Input:
        print('\033[0;33;48m[-]\033[0mYou must choose one function.\n')
    elif Input.isdecimal():
        Input = int(Input)
        if Input == 0:
            while True:
                s.send(b'0')
                d = s.recv(1024)
                data = d.decode('utf-8')
                if data == 'Bye':
                    break
            s.close()
            print('\033[0;32;48m[+]\033[0mGoodBye~\n')
            break
        elif Input == 1:
            Information(s)
        elif Input == 2:
            Process(s)
        elif Input == 3:
            print('3')
        else:
            print('\033[0;33;48m[-]\033[0mWrong ID. Please choose another one (? to get list).\n')
    elif Input == '?':
        Functions()
    else:
        print('\033[0;33;48m[-]\033[0mWrong Input.You must choose a correct function (? to get list).\n')
