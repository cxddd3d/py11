import socket
import sys

def main():
    # 创建socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置当服务器先close，即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时，可以立即使用该端口
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定IP和端口
    server_socket.bind(("", 8888))
    # 设置监听，最多允许5个客户端连接
    server_socket.listen(5)
    
    try:
        while True:
            # 等待客户端连接
            client_socket, client_addr = server_socket.accept()
            print(f"客户端 {client_addr} 已连接")
            
            # 接收客户端请求数据
            request_data = client_socket.recv(1024).decode('utf-8')
            print("请求头部信息：")
            print(request_data)
            
            # 构造响应数据
            response_start_line = "HTTP/1.1 200 OK\r\n"
            response_headers = "Server: MyPythonServer\r\n"
            response_body = "helloworld"
            response = response_start_line + response_headers + "\r\n" + response_body
            
            # 发送响应数据
            client_socket.send(response.encode('utf-8'))
            
            # 关闭客户端连接
            client_socket.close()
    except KeyboardInterrupt:
        # 处理Ctrl+C退出
        print("服务器关闭中...")
    finally:
        # 关闭服务器socket
        server_socket.close()
        print("服务器已关闭")

if __name__ == "__main__":
    main()
