# 作者: 王道 龙哥
# 2025年08月29日10时37分27秒
# xxx@qq.com
from time import ctime, sleep


def timefun(func):
    def wrapped_func(*args, **kwargs):
        print("%s called at %s" % (func.__name__, ctime()))
        return func(*args, **kwargs)  # 这里这么写，是因为被装饰的函数有返回值，所以这里需要返回值

    return wrapped_func


@timefun
def foo():
    return 'hello world'


result = foo()
print(result)

