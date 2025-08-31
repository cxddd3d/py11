# 作者: 王道 龙哥
# 2025年08月29日09时36分45秒
# xxx@qq.com

def w1(func):
    def inner():
        print('---正在验证权限---')
        func()
        print('---验证结束---')
    return inner


def f1():
    print('f1')


# 装饰器的内部实现
f1 = w1(f1)

f1()
