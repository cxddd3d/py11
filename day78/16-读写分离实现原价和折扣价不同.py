# 作者: 王道 龙哥
# 2025年08月25日16时19分35秒
# xxx@qq.com
class Goods:
    def __init__(self):
        self.original_price=100
        self.discount=0.8

    @property
    def price(self):
        return self.original_price*self.discount

    @price.setter
    def price(self, value):
        self.original_price=value

    @price.deleter  # 必须写，否则del 属性会出错
    def price(self):
        del self.original_price

apple=Goods()
print(apple.price)
apple.price=200
print(apple.price)