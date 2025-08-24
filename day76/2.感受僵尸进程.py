import time
from multiprocessing import Process
import os


def run_proc():
    """子进程要执行的代码"""
    # 打印自身进程id和父进程id,打印在一行
    print(f'我是子进程，子进程id {os.getpid()},父进程id {os.getppid()}')


if __name__ == "__main__":
    print(f'我是父进程，id是{os.getpid()}')
    p = Process(target=run_proc)
    p.start()  # 启动子进程
    while True:
        pass
