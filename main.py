#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入socket库:
import socket
import connect

# 变量定义
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
            print('1')
        elif Input == 2:
            print('2')
        elif Input == 3:
            print('3')
        else:
            print('\033[0;33;48m[-]\033[0mWrong ID. Please choose another one (? to get list).\n')
    elif Input == '?':
        Functions()
    else:
        print('\033[0;33;48m[-]\033[0mWrong Input.You must choose a correct function (? to get list).\n')
