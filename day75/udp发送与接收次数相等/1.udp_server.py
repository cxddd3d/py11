import socket

# 创建UDP套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定IP和端口
udp_socket.bind(("127.0.0.1", 2000))

# 接收数据
recv_data,client_addr = udp_socket.recvfrom(5)

print(f'接收到的数据是:{recv_data.decode("utf-8")},客户端的ip与端口{client_addr}')

# 接收数据
recv_data,client_addr = udp_socket.recvfrom(10)

print(f'第二次接收到的数据是:{recv_data.decode("utf-8")},客户端的ip与端口{client_addr}')
#关闭
udp_socket.close()