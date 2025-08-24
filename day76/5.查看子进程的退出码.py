import time
from multiprocessing import Process
import os


# 练习给子进程传参，父进程等待子进程结束

def run_proc(name, age, **kwargs):
    """子进程要执行的代码"""
    # 打印自身进程id和父进程id,打印在一行
    print(f'我是子进程，子进程id {os.getpid()},父进程id {os.getppid()}')
    for i in range(30):  # 循环30次，相当于3秒
        print(f"子进程运行中... {i + 1}/30")
        time.sleep(0.1)  # 每隔0.1秒打印一次
    print(name, age, kwargs)
    exit(0)


if __name__ == "__main__":
    print(f'我是父进程，id是{os.getpid()}')
    p = Process(target=run_proc, args=('张三', 18), kwargs={'height': 175})
    p.start()  # 启动子进程
    print('父进程开始等待')
    time.sleep(1)
    p.terminate() # 终止子进程
    p.join()  # 等待子进程结束，阻塞
    print(f'查看子进程的退出码{p.exitcode}')
    print('父进程结束')
    exit(0)