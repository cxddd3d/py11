import threading
import time

# 定义全局变量，线程之间共享
num = 0

def add_num():
    """子线程1：对全局变量num进行循环加1"""
    global num
    print(f"子线程1 ID: {threading.current_thread().ident} 开始执行")
    for i in range(100):
        num += 1
        time.sleep(0.1)  # 适当延时，便于观察

def read_num():
    """子线程2：不断读取全局变量num并打印"""
    global num
    print(f"子线程2 ID: {threading.current_thread().ident} 开始执行")
    for i in range(100):
        print(f"当前num的值为: {num}")
        time.sleep(0.1)  # 适当延时，便于观察

if __name__ == "__main__":
    print(f"主线程 ID: {threading.current_thread().ident}")
    
    # 创建两个子线程
    t1 = threading.Thread(target=add_num)
    t2 = threading.Thread(target=read_num)
    
    # 启动线程
    t1.start()
    t2.start()
    
    # 等待子线程执行完毕
    t1.join()
    t2.join()
    
    print("所有线程执行完毕")
    print(f"最终num的值为: {num}")
