import threading
import time

def worker1():
    """子线程1要执行的代码"""
    print(f"子线程1 ID: {threading.current_thread().ident} 开始执行")
    count = 0
    while True:
        count += 1
        print(f"子线程1 正在运行，计数: {count}")
        time.sleep(1)
        if count >= 50:  # 为了演示，设置一个退出条件
            print("子线程1 执行完毕")
            break
        pass
def worker2():
    """子线程2要执行的代码"""
    print(f"子线程2 ID: {threading.current_thread().ident} 开始执行")
    count = 0
    while True:
        count += 1
        print(f"子线程2 正在运行，计数: {count}")
        time.sleep(2)
        if count >= 30:  # 为了演示，设置一个退出条件
            print("子线程2 执行完毕")
            break
        pass

if __name__ == "__main__":
    print(f"主线程 ID: {threading.current_thread().ident}")
    
    # 创建两个子线程
    t1 = threading.Thread(target=worker1)
    t2 = threading.Thread(target=worker2)
    
    # 启动线程
    t1.start()
    t2.start()
    
    print("等待子线程执行完毕...")
    
    # 主线程等待子线程结束
    t1.join()
    t2.join()
    
    print("所有线程执行完毕")
