from socket import socket,AF_INET,SOCK_STREAM


#初始化套接字
tcp_server=socket(AF_INET,SOCK_STREAM)
#绑定ip和端口
tcp_server.bind(("127.0.0.1", 2000))
#监听
tcp_server.listen(10)

#accept  三次握手在这里
new_client_socket,client_addr=tcp_server.accept()
print(f'建立连接成功{client_addr}')

#接收数据
recv_data=new_client_socket.recv(5)
print(f'服务端端收到{recv_data.decode("utf8")}')


#接收数据
recv_data=new_client_socket.recv(10)
print(f'服务端端收到{recv_data.decode("utf8")}')

#关闭对象
new_client_socket.close()
tcp_server.close()

