# 作者: 王道 龙哥
# 2025年08月25日16时02分35秒
# xxx@qq.com
class Foo:
    def func(self):
        print('I am func')

    # 定义property属性
    @property
    def prop(self):
        return 100


f = Foo()
f.func()
price = f.prop  # property属性的作用是  能够让对象方法，像对象属性一样使用
print(price)
