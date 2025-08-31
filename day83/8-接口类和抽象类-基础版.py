# 作者: 王道 龙哥
# 2025年08月30日11时00分45秒
# xxx@qq.com


class Payment:
    def pay(self, money):
        e = Exception('缺少编写pay方法')
        raise e  # 手动抛异常


class Alipay(Payment):
    def paying(self, money):
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
