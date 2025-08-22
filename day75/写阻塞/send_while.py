from socket import socket, AF_INET, SOCK_STREAM
import time

def main():
    # 创建一个基于IPv4和TCP协议的套接字对象
    tcp_client = socket(AF_INET, SOCK_STREAM)

    # 定义服务器的IP地址和端口号
    server_addr = ("127.0.0.1", 2000)

    # 连接到指定的服务器和端口
    print("正在连接服务器...")
    tcp_client.connect(server_addr)
    print(f"已连接到服务器 {server_addr}")

    # 准备发送的数据
    data = "a" * 1000  # 创建一个包含1000个'a'的字符串
    data_bytes = data.encode('utf8')
    
    total_sent = 0  # 记录总共发送的字节数
    
    try:
        print("开始发送数据...")
        while True:
            # 发送数据
            sent = tcp_client.send(data_bytes)
            total_sent += sent
            
            # 打印发送的总字节数
            print(f"已发送总字节数: {total_sent}")
            
            # 短暂休眠，避免发送过快
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"发送数据时出错: {e}")
    finally:
        # 关闭套接字，释放资源
        tcp_client.close()
        print("客户端已关闭")

if __name__ == "__main__":
    main()
