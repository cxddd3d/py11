# 作者: 王道 龙哥
# 2025年08月29日11时03分45秒
# xxx@qq.com
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wper(*args, **kwargs):
        """
        这是装饰器函数的帮助
        """
        print('Calling decorated function...')
        return func(*args, **kwargs)

    return wper


@my_decorator
def example():
    """example函数的帮助"""
    print('Called example function')


@my_decorator
def example2():
    """example2函数的帮助"""
    print('Called example2 function')


print(example.__doc__)

print(example2.__doc__)
