import socket
# 创建UDP套接字
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#发送数据
server_addr=("127.0.0.1", 2000)
udp_client_socket.sendto('hello world'.encode('utf-8'),server_addr)

#接收数据
recv_data,_ = udp_client_socket.recvfrom(1024)

print(f'客户端接收到{recv_data.decode('utf-8')}')

udp_client_socket.close()