# 作者: 王道 龙哥
# 2025年08月30日11时00分45秒
# xxx@qq.com


from abc import ABC, abstractmethod


class Payment(ABC):
    """
    支付抽象类，当一个类继承这个类，不重写pay方法，在实例化就会抛出异常
    """
    @abstractmethod
    def pay(self, money):
        pass


class Alipay(Payment):
    def pay(self, money):
        print('支付宝支付了')


class Apppay(Payment):
    def pay(self, money):
        print('苹果支付了')


class Weicht(Payment):
    def pay(self, money):
        print('微信支付了')


def pay(payment, money):  # 支付函数，总体负责支付，对应支付的对象和要支付的金额
    payment.pay(money)


p = Alipay()
# pay(p, 200)
