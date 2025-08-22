from socket import socket, AF_INET, SOCK_STREAM

# 初始化套接字
tcp_server = socket(AF_INET, SOCK_STREAM)
# 绑定ip和端口
tcp_server.bind(("127.0.0.1", 2000))
# 监听
tcp_server.listen(10)

print("服务器启动成功，等待客户端连接...")

# accept 三次握手在这里
new_client_socket, client_addr = tcp_server.accept()
print(f'建立连接成功 {client_addr}')

# 通过无限循环让程序停下来，不做任何接收操作
try:
    while True:
        pass  # 空操作，让程序一直运行
except KeyboardInterrupt:
    print("\n程序被用户中断")
finally:
    # 关闭对象
    new_client_socket.close()
    tcp_server.close()
    print("服务器已关闭")
