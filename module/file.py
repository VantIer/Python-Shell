#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'File management'

__author__ = 'Vantler'

# 导入socket库:
import socket
import time
import module.connect as connect

# 变量定义
PATH = ''

#文字颜色
# 红色 \033[0;31;48m[!]\033[0m
# 绿色 \033[0;32;48m[+]\033[0m
# 黄色 \033[0;33;48m[-]\033[0m
# 蓝色 \033[0;36;48m[*]\033[0m

# 主流程
def File(sock):
    while True:
        Dir = ls(sock)
        if filemanage(sock, Dir):
            break
        time.sleep(0.1)

# 获取文件列表
def ls(sock):
    sock.send(b'3x00')
    data = connect.Receive(sock)
    ls = data.split('@V@',1)
    print('\n%s\n' % ls[1])
    return ls[0]

# 文件操作
def filemanage(sock, dir):
    print('\033[0;32;48m[+]\033[0m Orders:')
    print('[1] Parent directory')
    print('[2] Subdirectory')
    print('[3] Delete file')
    print('[4] New directory')
    print('[0] Exit\n')
    while True:
        Input = input('>>> \033[0;32;48m[%s]\033[0m: ' % dir)
        if not Input:
            print('\033[0;33;48m[-]\033[0mYou must choose one function.\n')
        elif Input.isdecimal():
            Input = int(Input)
            if Input == 0:
                return True
            elif Input == 1 or Input == 2 or Input == 3 or Input == 4:
                if Input == 1:
                    sock.send(b'3x01')
                elif Input == 2:
                    Input = input('>>> Directory name: ')
                    Input = Input.encode('utf-8')
                    sock.send(b'3x02||' + Input)
                elif Input == 3:
                    Input = input('>>> Directory / File name: ')
                    Input = Input.encode('utf-8')
                    sock.send(b'3x03||' + Input)
                elif Input == 4:
                    Input = input('>>> Directory name: ')
                    Input = Input.encode('utf-8')
                    sock.send(b'3x04||' + Input)
                return False
            else:
                print('\033[0;33;48m[-]\033[0mWrong ID. Please choose another one.\n')
        else:
            print('\033[0;33;48m[-]\033[0mWrong Input.You must choose a correct function.\n')

if __name__=='__main__':
    print('\nI think you should try \033[0;32;48mMAIN.PY\033[0m.    ㄟ( ▔, ▔ )ㄏ\n')