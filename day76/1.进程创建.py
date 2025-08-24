import time
from multiprocessing import Process

def run_proc():
    """子进程要执行的代码"""
    while True:
        print("----2----")
        time.sleep(1)


if __name__ == "__main__":
    p=Process(target=run_proc)
    p.start() # 启动子进程
    while True:
        print("----1----")
        time.sleep(1)