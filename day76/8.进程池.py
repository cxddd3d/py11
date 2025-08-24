from ast import main
from multiprocessing.pool import Pool
import time
import os
import random

def worker(msg):
    t_start = time.time()
    print("%s开始执行,进程号为%d" % (msg,os.getpid()))
    # random.random()随机生成0~1之间的浮点数
    time.sleep(random.random()*2) 
    t_stop = time.time()
    print(msg,"执行完毕，耗时%0.2f" % (t_stop-t_start))

if __name__ == "__main__":
    po=Pool(3)
    for i in range(10):
        po.apply_async(worker,(i,)) # 异步执行
    print('任务派遣完毕')
    po.close() # 关闭进程池，表示不能在添加新的任务
    time.sleep(2)
    po.terminate() # 终止进程池
    po.join() # 等待进程池中的所有任务完成
    print("----end----")