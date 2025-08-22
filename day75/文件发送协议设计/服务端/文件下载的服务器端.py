# 作者: 王道 龙哥
# 2025年08月21日16时05分11秒
# xxx@qq.com
from socket import socket,AF_INET,SOCK_STREAM,SO_REUSEADDR,SOL_SOCKET
import select
import sys
import struct
import os


#初始化套接字
tcp_server=socket(AF_INET,SOCK_STREAM)
#绑定ip和端口
tcp_server.bind(("127.0.0.1", 2000))
#监听
tcp_server.listen(10)

#设置reuse
tcp_server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
#accept  三次握手在这里
new_client_socket,client_addr=tcp_server.accept()
print(f'建立连接成功 {client_addr}')

#先发文件名file，再发文件内容
file_name='第四讲视频.mp4'
train_head=struct.pack('I',len(file_name.encode('utf-8')))
print(train_head)

#发送文件名
new_client_socket.send(train_head) #发送文件名长度，4个字节，火车头
new_client_socket.send(file_name.encode('utf-8')) #发送文件名，火车身

#发送文件内容
#获取文件内容长度
file_size=os.path.getsize(file_name)
train_head=struct.pack('I',file_size)
new_client_socket.send(train_head) #发送文件内容长度，4个字节，火车头
#发送文件内容，火车身
with open(file_name,'rb') as f:
    while True:
        data=f.read(1024)
        if not data:
            break
        new_client_socket.send(data)
#关闭套接字
new_client_socket.close()
tcp_server.close()