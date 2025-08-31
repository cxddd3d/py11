# 作者: 王道 龙哥
# 2025年08月29日16时46分15秒
# xxx@qq.com
class ObjectCreator:
    pass


class ObjectCreator2:
    pass


def echo(myclass):
    obj = myclass()
    print(obj)


ObjectCreator = ObjectCreator2
print(ObjectCreator)
echo(ObjectCreator)
