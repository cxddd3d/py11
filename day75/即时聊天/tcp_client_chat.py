from socket import socket, AF_INET, SOCK_STREAM
import time,sys
import select
# 创建一个基于IPv4和TCP协议的套接字对象
tcp_client = socket(AF_INET, SOCK_STREAM)

# 定义服务器的IP地址和端口号
server_addr = ("127.0.0.1", 2000)

# 连接到指定的服务器和端口
tcp_client.connect(server_addr)

#epoll初始化及注册标准输入，套接字
epoll_fd=select.epoll()
epoll_fd.register(sys.stdin.fileno(),select.EPOLLIN)
epoll_fd.register(tcp_client.fileno(),select.EPOLLIN)


while True:
    #epoll等待事件发生,poll阻塞的
    events=epoll_fd.poll()
    for fd,event in events:
        if fd==sys.stdin.fileno():#标准输入缓存区有数据
            #读取input
            send_data=input()
            #发送数据
            tcp_client.send(send_data.encode('utf8'))
        elif fd==tcp_client.fileno():#套接字有数据
            #接收数据
            recv_data=tcp_client.recv(1024)
            if not recv_data:
                tcp_client.close()
                exit() #退出程序
            print(recv_data.decode("utf8"))



# 关闭套接字，释放资源
tcp_client.close()