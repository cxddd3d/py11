# 作者: 王道 龙哥
# 进程池中的子进程通信示例：一个子进程写数据，另一个子进程读数据
from multiprocessing import Pool, Manager
import time
import os
import random

def write_task(q):
    """
    写入队列的任务
    """
    print(f"写入进程 PID: {os.getpid()}")
    for value in ['A', 'B', 'C', 'D', 'E']:
        print(f"写入数据: {value}")
        q.put(value)
        time.sleep(random.random())  # 随机暂停一段时间

def read_task(q):
    """
    读取队列的任务
    """
    print(f"读取进程 PID: {os.getpid()}")
    count = 0
    # 最多尝试10次读取数据
    while count < 10:
        if not q.empty():
            value = q.get()
            print(f"读取到数据: {value}")
        else:
            print("队列为空，等待数据...")
            time.sleep(0.5)
        count += 1

if __name__ == "__main__":
    # 创建进程池
    po = Pool(2)
    
    # 使用Manager创建可在进程间共享的队列
    manager = Manager()
    queue = manager.Queue()
    
    # 添加写入任务到进程池
    po.apply_async(write_task, (queue,))
    
    # 添加读取任务到进程池
    po.apply_async(read_task, (queue,))
    
    print('任务派遣完毕')
    
    # 关闭进程池，表示不能再添加新的任务
    po.close()
    
    # 等待进程池中的所有任务完成
    po.join()
    
    print("----所有任务执行完毕----")
