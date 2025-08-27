import socket
import sys
import os
import select


class WebServer:
    def __init__(self, port=8888):
        """初始化Web服务器"""
        self.port = port
        self.html_root_path = "./html"
        # 创建socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置当服务器先close，即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时，可以立即使用该端口
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置为非阻塞模式
        self.server_socket.setblocking(False)
        # 绑定IP和端口
        self.server_socket.bind(("192.168.19.128", self.port))
        # 设置监听，最多允许5个客户端连接
        self.server_socket.listen(5)
        print(f"服务器已启动，监听端口：{self.port}")
        
        # 创建epoll对象
        self.epoll = select.epoll()
        # 注册服务器socket的可读事件到epoll
        self.epoll.register(self.server_socket.fileno(), select.EPOLLIN)
        
        # 用于保存客户端连接的字典，格式为 {文件描述符: socket对象}
        self.connections = {}
        # 用于保存客户端地址的字典，格式为 {文件描述符: 客户端地址}
        self.addresses = {}

    def handle_request(self, client_socket, client_addr):
        """处理客户端请求"""
        try:
            # 接收客户端请求数据
            request_data = client_socket.recv(40960)
            
            # 如果接收到的数据为空，说明客户端已经关闭连接
            if not request_data:
                return False
                
            request_text = request_data.decode('utf-8')
            print(f"客户端 {client_addr} 的请求头部信息：")
            print(request_text)

            # 解析请求路径
            request_lines = request_text.split('\r\n')
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
            
            return True
        except Exception as e:
            print(f"处理客户端请求时发生错误: {e}")
            return False

    def start(self):
        """启动Web服务器"""
        try:
            while True:
                # 等待事件发生，timeout为1秒
                events = self.epoll.poll(1)
                
                # 处理事件
                for fd, event in events:
                    # 如果是服务器socket可读，说明有新的连接请求
                    if fd == self.server_socket.fileno():
                        client_socket, client_addr = self.server_socket.accept()
                        print(f"客户端 {client_addr} 已连接")
                        
                        # 设置客户端socket为非阻塞
                        client_socket.setblocking(False)
                        
                        # 注册客户端socket的可读事件到epoll
                        self.epoll.register(client_socket.fileno(), select.EPOLLIN)
                        
                        # 保存客户端连接
                        self.connections[client_socket.fileno()] = client_socket
                        self.addresses[client_socket.fileno()] = client_addr
                    
                    # 如果是客户端socket可读，说明有数据可以接收
                    elif event & select.EPOLLIN:
                        # 处理客户端请求
                        client_socket = self.connections[fd]
                        client_addr = self.addresses[fd]
                        
                        # 如果处理请求失败或客户端关闭连接，则关闭连接
                        self.handle_request(client_socket, client_addr)

                        # 从epoll中注销客户端socket
                        self.epoll.unregister(fd)
                        # 关闭客户端socket
                        client_socket.close()
                        print(f"客户端 {client_addr} 连接已关闭")
                        # 从字典中删除客户端信息
                        del self.connections[fd]
                        del self.addresses[fd]
                    
                    # 如果有错误发生，关闭连接
                    elif event & (select.EPOLLHUP | select.EPOLLERR):
                        client_addr = self.addresses[fd]
                        print(f"客户端 {client_addr} 连接出错或断开")
                        # 从epoll中注销客户端socket
                        self.epoll.unregister(fd)
                        # 关闭客户端socket
                        self.connections[fd].close()
                        # 从字典中删除客户端信息
                        del self.connections[fd]
                        del self.addresses[fd]
                
        except KeyboardInterrupt:
            # 处理Ctrl+C退出
            print("服务器关闭中...")
        finally:
            # 关闭epoll
            self.epoll.unregister(self.server_socket.fileno())
            self.epoll.close()
            # 关闭所有客户端连接
            for conn in self.connections.values():
                conn.close()
            # 关闭服务器socket
            self.server_socket.close()
            print("服务器已关闭")


def main():
    """主函数"""
    server = WebServer(port=8888)
    server.start()


if __name__ == "__main__":
    main()
