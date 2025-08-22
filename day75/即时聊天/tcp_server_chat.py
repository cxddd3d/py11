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

#accept  三次握手在这里
new_client_socket,client_addr=tcp_server.accept()
print(f'建立连接成功{client_addr}')

#epoll初始化及注册标准输入，套接字
epoll_fd=select.epoll()
epoll_fd.register(sys.stdin.fileno(),select.EPOLLIN)
epoll_fd.register(new_client_socket.fileno(),select.EPOLLIN)

#tcp当对方关闭连接时，new_client_socket是一直可读的，所以需要判断是否为空

while True:
    #epoll等待事件发生,poll阻塞的
    events=epoll_fd.poll()
    for fd,event in events:
        if fd==sys.stdin.fileno():#标准输入缓存区有数据
            #读取input
            send_data=input()
            #发送数据
            new_client_socket.send(send_data.encode('utf8'))
        elif fd==new_client_socket.fileno():
            #接收数据
            recv_data=new_client_socket.recv(1024)
            if not recv_data:
                new_client_socket.close()
                tcp_server.close()
                exit() #退出程序
            print(recv_data.decode("utf8"))

#关闭对象
new_client_socket.close()
tcp_server.close()

