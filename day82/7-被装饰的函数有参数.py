# 作者: 王道 龙哥
# 2025年08月29日10时32分23秒
# xxx@qq.com
from time import ctime, sleep


def timefun(func):
    def wrapped_func(a, b):
        # ctime的作用是返回当前时间，格式是字符串类型
        print("%s called at %s" % (func.__name__, ctime()))
        print(a, b)
        func(a, b)

    return wrapped_func


@timefun
def foo(a, b):
    print(a + b)

foo(1, 2)