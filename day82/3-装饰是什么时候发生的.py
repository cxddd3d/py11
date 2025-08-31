# 作者: 王道 龙哥
# 2025年08月29日09时47分01秒
# xxx@qq.com
def set_func(func):
    print("---开始进行装饰")

    def call_func(a):
        print("---这是权限验证1----")
        print("---这是权限验证2----")
        func(a)

    return call_func


@set_func  # 相当于 test1 = set_func(test1)
def test1(num):
    print("-----test1----%d" % num)


