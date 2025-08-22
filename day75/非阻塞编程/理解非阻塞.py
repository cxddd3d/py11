from socket import socket, AF_INET, SOCK_STREAM
import time
import sys

def main():
    # 初始化套接字
    tcp_server = socket(AF_INET, SOCK_STREAM)
    # 绑定ip和端口
    tcp_server.bind(("127.0.0.1", 2000))
    # 监听
    tcp_server.listen(10)
    
    # 设置服务器套接字为非阻塞模式
    tcp_server.setblocking(False)
    
    # 存储客户端连接列表
    client_sockets = []
    
    print("服务器启动成功，等待客户端连接...")
    
    try:
        while True:
            # 尝试接受新连接
            try:
                new_client_socket, client_addr = tcp_server.accept()
                print(f'\n建立连接成功: {client_addr}')
                
                # 设置客户端套接字为非阻塞模式
                new_client_socket.setblocking(False)
                
                # 保存客户端连接
                client_sockets.append(new_client_socket)
                
            except BlockingIOError:
                # 非阻塞模式下，如果没有连接请求，accept会抛出异常
                pass
            except Exception as e:
                print(f"接受连接时出错: {e}")
            
            # 处理现有连接
            for client_socket in client_sockets[:]:  # 使用切片创建副本，以便在循环中安全删除元素
                try:
                    # 尝试接收数据
                    recv_data = client_socket.recv(1024)
                    if not recv_data:  # 客户端断开连接
                        print(f'\n客户端断开连接')
                        # 关闭连接
                        client_socket.close()
                        # 从列表中删除
                        client_sockets.remove(client_socket)
                    else:
                        # 处理接收到的数据
                        msg = recv_data.decode("utf8")
                        print(f"\n收到消息: {msg}")
 
                except BlockingIOError:
                    # 非阻塞模式下，如果没有数据可读，recv会抛出异常
                    pass
                except Exception as e:
                    print(f'\n处理客户端数据异常: {e}')
                    # 关闭连接
                    client_socket.close()
                    # 从列表中删除
                    if client_socket in client_sockets:
                        client_sockets.remove(client_socket)
            
            # 短暂休眠，避免CPU占用过高
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n服务器正在关闭...")
    finally:
        # 关闭所有连接
        for client_socket in client_sockets:
            client_socket.close()
        tcp_server.close()
        print("服务器已关闭")

if __name__ == "__main__":
    main()

