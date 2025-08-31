# 作者: 王道 龙哥
# 2025年08月29日10时35分37秒
# xxx@qq.com
def set_func(func):
    print("---开始进行装饰")

    def call_func(*args, **kwargs):
        print("---这是权限验证1----")
        print("---这是权限验证2----")
        # func(args, kwargs)  # 不行，相当于传递了2个参数 ：1个元组，1个字典
        func(*args, **kwargs)  # 拆包的过程

    return call_func


@set_func
def test1(num, *args, **kwargs):
    print("-----test1----%d" % num)
    print("-----test1----", args)
    print("-----test1----", kwargs)


test1(100)
print('-'*50)
test1(100, 200)
print('-'*50)
test1(100, 200, 300, mm=100)
