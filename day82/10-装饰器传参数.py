# 作者: 王道 龙哥
# 2025年08月29日10时43分41秒
# xxx@qq.com
def timefun_arg(pre="hello"):
    def timefun(func):
        def wrapped_func():
            print("%s called at %s" % (func.__name__, pre))
            return func()

        return wrapped_func

    return timefun


@timefun_arg('wangdao')
def foo():
    print("I am foo")


@timefun_arg("python")
def too():
    print("I am too")

foo()

too()