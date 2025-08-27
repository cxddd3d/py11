import socket
import sys
import os
import threading


class WebServer:
    def __init__(self, port=8888):
        """初始化Web服务器"""
        self.port = port
        self.html_root_path = "./html"
        # 创建socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置当服务器先close，即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时，可以立即使用该端口
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定IP和端口
        self.server_socket.bind(("", self.port))
        # 设置监听，最多允许5个客户端连接
        self.server_socket.listen(5)
        print(f"服务器已启动，监听端口：{self.port}")

    def handle_client(self, client_socket, client_addr):
        """处理客户端请求的子进程函数"""
        print(f"子进程 {os.getpid()} 处理客户端 {client_addr} 的请求")
        
        try:
            # 接收客户端请求数据
            request_data = client_socket.recv(40960).decode('utf-8')
            print("请求头部信息：")
            print(request_data)

            # 解析请求路径
            request_lines = request_data.split('\r\n')
            if len(request_lines) > 0:
                request_line = request_lines[0]  # 获取请求行
                file_path = request_line.split(' ')[1]  # 获取请求的文件路径
                
                # 如果请求的是根路径，默认返回index.html
                if file_path == '/':
                    file_path = '/index.html'
                
                # 构建文件的完整路径
                file_name = self.html_root_path + file_path
                
                try:
                    # 打开文件，读取内容
                    with open(file_name, 'rb') as file:
                        file_content = file.read()
                    
                    # 构造响应数据
                    response_start_line = "HTTP/1.1 200 OK\r\n"
                    response_headers = "Server: MyPythonServer\r\n"
                    
                    # 发送响应头
                    response_headers_bytes = (response_start_line + response_headers + "\r\n").encode('utf-8')
                    client_socket.send(response_headers_bytes)
                    
                    # 发送响应体
                    client_socket.send(file_content)
                except FileNotFoundError:
                    # 文件不存在，返回404
                    response_start_line = "HTTP/1.1 404 Not Found\r\n"
                    response_headers = "Server: MyPythonServer\r\n"
                    response_headers += "Content-Type: text/html; charset=utf-8\r\n"
                    response_body = "文件不存在！"
                    response = response_start_line + response_headers + "\r\n" + response_body
                    client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"处理客户端请求时发生错误: {e}")
        finally:
            # 关闭客户端连接
            client_socket.close()
            print(f"客户端 {client_addr} 连接已关闭")

    def start(self):
        """启动Web服务器"""
        try:
            while True:
                # 等待客户端连接
                client_socket, client_addr = self.server_socket.accept()
                print(f"客户端 {client_addr} 已连接")
                
                # 创建子线程处理客户端请求
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_addr)
                )
                # 设置为守护线程，主线程退出时子线程也会退出
                client_thread.daemon = True
                # 启动子线程
                client_thread.start()
                
        except KeyboardInterrupt:
            # 处理Ctrl+C退出
            print("服务器关闭中...")
        finally:
            # 关闭服务器socket
            self.server_socket.close()
            print("服务器已关闭")


def main():
    """主函数"""
    server = WebServer(port=8888)
    server.start()


if __name__ == "__main__":
    main()
