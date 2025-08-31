# 作者: 王道 龙哥
# 2025年08月30日09时27分42秒
# xxx@qq.com
def choose_class(name):
    if name == 'foo':
        class Foo(object):
            pass

        return Foo  # 返回的是类，不是类的实例
    else:
        class Bar(object):
            pass

        return Bar

obj=choose_class('bar')
print(obj)

