# 导入socket库:
import socket

# 变量定义
IP = '127.0.0.1'
PORT = 9481

#文字颜色
# 红色 \033[0;31;48m[!]\033[0m
# 绿色 \033[0;32;48m[+]\033[0m
# 黄色 \033[0;33;48m[-]\033[0m

# 【函数】获取目标地址:
def Target():
    global IP,PORT
    Input = input('>>> Target IP/Host: ')
    if Input:
        IP = Input
    print('\033[0;32;48m[+]\033[0mYour Target IP/Host is %s\n' %IP)
    while True:
        Input = input('>>> PORT: ')
        if not Input:
            print('\033[0;32;48m[+]\033[0mYour Target Port is %d\n' %PORT)
            break
        if Input.isdecimal():
            Input = int(Input)
            if Input >=1 and Input <= 65535:
                PORT = Input
                Input = None
                print('\033[0;32;48m[+]\033[0mYour Target Port is %d\n' %PORT)
                break
        print('\n\033[0;31;48m[!]\033[0mERROR: Please input a VALID port.\n')
    return
print('\n\n')
print('          \033[0;33;48m\\\\\033[0m    \033[0;34;48mPY\033[0m     \033[0;31;48m//\033[0m')
print('           \033[0;33;48m\\\\\033[0m  \033[0;32;48mShell\033[0m  \033[0;31;48m//\033[0m')
print('            \033[0;33;48m\\\\\033[0m       \033[0;31;48m//\033[0m')
print('             \033[0;33;48m\\\\\033[0m     \033[0;31;48m//\033[0m')
print('              \033[0;33;48m\\\\\033[0m   \033[0;31;48m//\033[0m')
print('               \033[0;33;48m\\\\\033[0m \033[0;31;48m//\033[0m')
print('                \033[0;33;48m\\\033[0m\033[0;36;48mV\033[0m\033[0;31;48m/\033[0m')
print('\n\n')

# 创建连接
while True:
    Target()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s.connect_ex((IP, PORT)) != 0:
        print('\033[0;31;48m[!]\033[0mERROR: Connection Failed.\n')
    else:
        break

#功能函数
iptemp = IP.encode('ascii')
print(b'GET / HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n' %iptemp)
s.send(b'GET / HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n' %iptemp)
buffer = []
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