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
# 功能
print('\033[0;32;48m[+]\033[0mLogin Successful.\n')
print('\033[0;32;48m[+]\033[0mLogin Successful.\n')
s.close()
