import socket

# 创建UDP套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定IP和端口
udp_socket.bind(("127.0.0.1", 2000))

# 接收数据
recv_data,client_addr = udp_socket.recvfrom(1024)

print(f'接收到的数据是:{recv_data.decode("utf-8")},客户端的ip与端口{client_addr}')

#发送数据
udp_socket.sendto('hello python'.encode('utf-8'),client_addr)

#关闭
udp_socket.close()