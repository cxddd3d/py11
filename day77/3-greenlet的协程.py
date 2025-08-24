# 作者: 王道 龙哥
# 2025年08月23日10时32分08秒
# xxx@qq.com
from greenlet import greenlet
import time


def test1():
    while True:
        print("---A--")
        gr2.switch()
        time.sleep(0.5)


def test2():
    while True:
        print("---B--")
        gr1.switch()
        time.sleep(0.5)


gr1 = greenlet(test1) #协程1   
gr2 = greenlet(test2) #协程2

# 切换到gr1中运行
gr1.switch()
