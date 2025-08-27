# 作者: 王道 龙哥
# 2025年08月25日16时13分36秒
# xxx@qq.com
class Goods:
    @property
    def price(self):
        print('price get')

    @price.setter
    def price(self, value):
        print(f'price set {value}')

    @price.deleter  # 必须写，否则del 属性会出错
    def price(self):
        pass


apple = Goods()

apple.price = 100

del apple.price
