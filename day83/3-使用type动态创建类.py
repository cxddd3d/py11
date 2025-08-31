# 作者: 王道 龙哥
# 2025年08月30日09时33分34秒
# xxx@qq.com

class Foo(object):
    bar = True


def echo_bar(self):
    print(self.bar)


@staticmethod
def test_static():
    print("static method ....")


Test2 = type("Test2", (Foo,), {'echo_bar': echo_bar, 'test_static': test_static})  # type返回的是类

obj = Test2()

print(Test2)
print(Test2.bar)
print(obj)
obj.echo_bar()
Test2.test_static()
