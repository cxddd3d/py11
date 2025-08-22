from socket import socket, AF_INET, SOCK_STREAM
import time
# 创建一个基于IPv4和TCP协议的套接字对象
tcp_client = socket(AF_INET, SOCK_STREAM)

# 定义服务器的IP地址和端口号
server_addr = ("127.0.0.1", 2000)

# 连接到指定的服务器和端口
tcp_client.connect(server_addr)

# 发送数据，数据必须是bytes类型
tcp_client.send(b'hello python')


time.sleep(1)
# 关闭套接字，释放资源
tcp_client.close()