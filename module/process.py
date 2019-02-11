#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Process management'

__author__ = 'Vantler'

# 导入socket库:
import socket
import time
import module.connect as connect

# 进程管理
def Process(sock):
    sock.send(b'2')
    data = connect.Receive(sock)
    print('\n%s\n' % data)
    while True:
        if Processmanage(sock):
            break
    return

# 进程操作
def Processmanage(sock):
    print('\033[0;32;48m[+]\033[0m Orders:')
    print('[1] Kill by Name (Only for Win)')
    print('[2] Kill by ID')
    print('[3] Process List')
    print('[0] Exit\n')
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
                    data = connect.Receive(sock)
                    print('\n%s\n' % data)
                    return False
                d = sock.recv(1024)
                data = d.decode('utf-8')
                print('\n%s\n' % data)
                return False
            else:
                print('\033[0;33;48m[-]\033[0mWrong ID. Please choose another one.\n')
        else:
            print('\033[0;33;48m[-]\033[0mWrong Input.You must choose a correct function.\n')

if __name__=='__main__':
    print('\nI think you should try \033[0;32;48mMAIN.PY\033[0m.    ㄟ( ▔, ▔ )ㄏ\n')