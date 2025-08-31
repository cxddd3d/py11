# 作者: 王道 龙哥
# 2025年08月29日09时49分36秒
# xxx@qq.com
def add_first(func):
    print("---开始进行装饰权限1的功能---")

    def call_func(*args, **kwargs):
        print("---这是权限验证1----")
        return func(*args, **kwargs)

    return call_func


def add_second(func):
    print("---开始进行装饰权限2的功能---")

    def call_func(*args, **kwargs):
        print("---这是权限验证2----")
        return func(*args, **kwargs)

    return call_func


@add_first
@add_second
def test1():
    print("-----test1----")


# 离的近的先装饰,先装饰后执行

test1()
