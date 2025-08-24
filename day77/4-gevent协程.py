# 作者: 王道 龙哥
# 2025年08月23日
import gevent
import time
import random
from gevent import monkey

# 打补丁，将标准库中的耗时操作替换为gevent的协程版本
monkey.patch_all()

def work(n, count):
    """
    协程工作函数
    :param n: 协程编号
    :param count: 循环次数
    """
    for i in range(count):
        print(f"协程{n}执行第{i+1}次任务")
        # 模拟随机耗时操作
        sleep_time = random.uniform(0.05, 0.3)
        gevent.sleep(sleep_time)

def main():
    # 创建3个协程
    count = 5  # 每个协程执行的循环次数
    g1 = gevent.spawn(work, 1, count)
    g2 = gevent.spawn(work, 2, count)
    g3 = gevent.spawn(work, 3, count)
    
    # 等待所有协程执行完毕
    gevent.joinall([g1, g2, g3])

if __name__ == "__main__":
    main()
