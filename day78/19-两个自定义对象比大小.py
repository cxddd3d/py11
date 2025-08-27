# 作者: 王道 龙哥
# 2025年08月25日16时37分43秒
# xxx@qq.com
class Goods(object):

    def __init__(self, price):
        # 原价
        self.price = price

    def __gt__(self, other):
        return self.price > other.price


a = Goods(11)
b = Goods(10)
print(a > b)
