# 作者: 王道 龙哥
# 2025年08月23日10时27分43秒
# xxx@qq.com
import time


def work1():
    while True:
        print("----work1---")
        yield
        time.sleep(0.5)


def work2():
    while True:
        print("----work2---")
        yield
        time.sleep(0.5)


def main():
    w1 = work1()  # 协程1
    w2 = work2()  # 协程2
    while True:
        next(w1)
        next(w2)


if __name__ == "__main__":
    main()
