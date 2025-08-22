import socket
# 创建UDP套接字
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#发送数据
server_addr=("127.0.0.1", 2000)
udp_client_socket.sendto('hello world'.encode('utf-8'),server_addr)


udp_client_socket.close()