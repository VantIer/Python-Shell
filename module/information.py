#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Information management'

__author__ = 'Vantler'

# 导入socket库:
import socket
import time
import module.connect as connect

# 系统信息
def Information(sock):
    sock.send(b'1x00')
    data = connect.Receive(sock)
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
                data = connect.Receive(sock)
                print('\n%s\n' % data)
                return False
            else:
                print('\033[0;33;48m[-]\033[0mWrong ID. Please choose another one.\n')
        else:
            print('\033[0;33;48m[-]\033[0mWrong Input.You must choose a correct function.\n')

if __name__=='__main__':
    print('\nI think you should try \033[0;32;48mMAIN.PY\033[0m.    ㄟ( ▔, ▔ )ㄏ\n')