import threading
import time

# 定义全局变量
balance = 1000  # 假设这是银行账户余额
# 创建互斥锁
lock = threading.Lock()

def withdraw(amount):
    """模拟取款操作"""
    global balance
    
    # 获取互斥锁
    lock.acquire()
    try:
        # 模拟读取当前余额
        current_balance = balance
        print(f"线程 {threading.current_thread().name} 读取到余额: {current_balance}")
        
        # 模拟网络延迟或其他耗时操作
        time.sleep(0.1)
        
        # 计算取款后的余额
        new_balance = current_balance - amount
        
        # 模拟更新余额操作
        balance = new_balance
        print(f"线程 {threading.current_thread().name} 取款 {amount}元后，余额变为: {new_balance}")
    finally:
        # 释放互斥锁
        lock.release()

if __name__ == "__main__":
    print("=== 并发问题演示：使用互斥锁解决多线程取款问题 ===")
    print(f"初始账户余额: {balance}元")
    
    # 创建多个线程同时取款
    threads = []
    for i in range(5):
        t = threading.Thread(target=withdraw, args=(200,), name=f"取款线程-{i+1}")
        threads.append(t)
    
    # 启动所有线程
    for t in threads:
        t.start()
    
    # 等待所有线程执行完毕
    for t in threads:
        t.join()
    
    print(f"理论上余额应该是: {1000 - 5*200}元")
    print(f"实际余额是: {balance}元")
    print("通过使用互斥锁，成功解决了线程并发访问导致的数据错误问题！")
