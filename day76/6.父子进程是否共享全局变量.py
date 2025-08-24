# 作者: 王道 龙哥
# 2025年08月22日11时22分17秒
# xxx@qq.com
from multiprocessing import Process
import os
import time
#不共享全局变量
nums = [11, 22]

def work1():
    """子进程要执行的代码"""
    print("in process1 pid=%d ,nums=%s" % (os.getpid(), nums))
    for i in range(3):
        nums.append(i)
        time.sleep(1)
        print("in process1 pid=%d ,nums=%s" % (os.getpid(), nums))

def work2():
    """子进程要执行的代码"""
    for i in range(3):
        time.sleep(1)
        print("in process2 pid=%d ,nums=%s" % (os.getpid(), nums))

if __name__ == '__main__':
    p1 = Process(target=work1)
    p1.start()


    p2 = Process(target=work2)
    p2.start()
    p1.join()
    p2.join()