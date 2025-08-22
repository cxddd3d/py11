from socket import socket,AF_INET,SOCK_STREAM
import select
import sys
#server先说话

#初始化套接字
tcp_server=socket(AF_INET,SOCK_STREAM)
#绑定ip和端口
tcp_server.bind(("127.0.0.1", 2000))
#监听
tcp_server.listen(10)

#设置为非阻塞模式
tcp_server.setblocking(False)

#epoll初始化及注册标准输入，套接字
epoll_fd=select.epoll()
epoll_fd.register(sys.stdin.fileno(),select.EPOLLIN)
epoll_fd.register(tcp_server.fileno(),select.EPOLLIN)

#存储客户端连接，字典格式，key是套接字的fd，value是套接字
client_sockets = {}

while True:
    #epoll等待事件发生,poll阻塞的
    events=epoll_fd.poll()
    for fd,event in events:
        if fd == tcp_server.fileno():  # 有新的客户端连接
            new_client_socket,client_addr=tcp_server.accept()
            print(f'建立连接成功{client_addr}')
            # 设置为非阻塞模式
            # new_client_socket.setblocking(False)
            # 注册新客户端到epoll
            epoll_fd.register(new_client_socket.fileno(),select.EPOLLIN)
            # 保存客户端连接,key是套接字的fd，value是套接字
            client_sockets[new_client_socket.fileno()] = new_client_socket
        else:  # 客户端有数据
            client_socket = client_sockets.get(fd)
            if client_socket:
                #接收数据
                try:
                    recv_data=client_socket.recv(1024)
                    if not recv_data:  # 客户端断开连接
                        print(f'{fd}客户端断开连接')
                        # 解除注册
                        epoll_fd.unregister(fd)
                        # 关闭连接
                        client_socket.close()
                        # 从字典中删除
                        del client_sockets[fd]
                    else:
                        # 将消息转发给除了发送者以外的所有客户端
                        for other_fd, other_socket in client_sockets.items():
                            if other_fd != fd:  # 不发送给消息来源的客户端
                                try:
                                    other_socket.send(recv_data)
                                except:
                                    pass  # 发送失败则忽略
                except Exception as e:
                    print(f'接收数据异常: {e}')
                    # 解除注册
                    epoll_fd.unregister(fd)
                    # 关闭连接
                    client_socket.close()
                    # 从字典中删除
                    del client_sockets[fd]

#关闭对象
for client_socket in client_sockets.values():
    client_socket.close()
tcp_server.close()
