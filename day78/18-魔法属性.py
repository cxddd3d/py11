# 作者: 王道 龙哥
# 2025年08月25日16时31分25秒
# xxx@qq.com
class Foo:
    """ 描述类信息，这是用于看片的神奇 """

    def func(self):
        pass


print(Foo.__doc__)

from test1 import Person

obj = Person()
print(obj.__module__)
print(obj.__class__)


class Province(object):
    country = 'China'

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def func(self, *args, **kwargs):
        print('func')


shenzhen = Province('深圳', 10)
print(Province.__dict__)
print(shenzhen.__dict__)
