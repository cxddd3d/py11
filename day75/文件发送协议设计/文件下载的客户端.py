# 作者: 王道 龙哥
# 2025年08月21日16时05分21秒
# xxx@qq.com

from socket import socket, AF_INET, SOCK_STREAM
import os
import struct

def main():
    # 创建一个基于IPv4和TCP协议的套接字对象
    tcp_client = socket(AF_INET, SOCK_STREAM)

    # 定义服务器的IP地址和端口号
    server_addr = ("127.0.0.1", 2000)

    try:
        # 连接到指定的服务器和端口
        print("正在连接服务器...")
        tcp_client.connect(server_addr)
        print(f"已连接到服务器 {server_addr}")


        # 接收文件名长度
        file_name_len_bytes = tcp_client.recv(4) #接火车头
        file_name_len = struct.unpack('I', file_name_len_bytes)[0]

        # 接收文件名
        file_name_bytes = tcp_client.recv(file_name_len)
        file_name = file_name_bytes.decode('utf8')
        print(f"准备下载文件: {file_name}")

        # 接收文件大小
        file_size_bytes = tcp_client.recv(4)
        file_size = struct.unpack('I', file_size_bytes)[0]
        print(f"文件大小: {file_size} 字节")


        # 准备接收文件内容
        received_size = 0

        with open(file_name, 'wb') as f:
            while received_size < file_size:
                # 计算本次应该接收的大小
                size_to_receive = min(1024, file_size - received_size)
                
                # 接收数据
                data = tcp_client.recv(size_to_receive)
                if not data:
                    break
                
                # 写入文件
                f.write(data)
                received_size += len(data)
                
                # 显示下载进度
                progress = received_size / file_size * 100
                print(f"\r下载进度: {progress:.2f}%", end="")

        print("\n文件下载完成!")


    except Exception as e:
        print(f"下载过程中出错: {e}")
    finally:
        # 关闭套接字，释放资源
        tcp_client.close()
        print("客户端已关闭")

if __name__ == "__main__":
    main()
