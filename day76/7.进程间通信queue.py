# 作者: 王道 龙哥
# 进程间通信示例：父进程写数据，子进程读数据
from multiprocessing import Process, Queue
import time
import os

def write_task(q):
    """
    父进程要执行的写入队列的任务
    """
    print(f"写入进程 PID: {os.getpid()}")
    for value in ['A', 'B', 'C', 'D', 'E']:
        print(f"写入数据: {value}")
        q.put(value)
        time.sleep(1)  # 每次写入后暂停1秒

def read_task(q):
    """
    子进程要执行的读取队列的任务
    """
    print(f"读取进程 PID: {os.getpid()}, 父进程 PID: {os.getppid()}")
    while True:
        if not q.empty():
            value = q.get()
            print(f"读取到数据: {value}")
        else:
            time.sleep(0.5)  # 队列为空时等待0.5秒

if __name__ == "__main__":
    # 创建队列
    q = Queue()
    
    # 创建子进程
    p = Process(target=read_task, args=(q,))
    p.start()
    
    # 父进程写入数据
    write_task(q)
    
    # 等待子进程结束
    p.terminate()  # 由于子进程是死循环，需要手动终止
    p.join()
    
    print("所有数据处理完毕")
