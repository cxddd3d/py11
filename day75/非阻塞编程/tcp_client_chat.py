from socket import socket, AF_INET, SOCK_STREAM
import time
# 创建一个基于IPv4和TCP协议的套接字对象
tcp_client = socket(AF_INET, SOCK_STREAM)

# 定义服务器的IP地址和端口号
server_addr = ("127.0.0.1", 2000)

# 连接到指定的服务器和端口
tcp_client.connect(server_addr)


tcp_client.send('我是张三'.encode('utf8'))



# 关闭套接字，释放资源
tcp_client.close()