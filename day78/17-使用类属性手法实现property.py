# 作者: 王道 龙哥
# 2025年08月25日16时23分36秒
# xxx@qq.com
class Foo(object):
    def get_bar(self):
        print("getter...")
        return 'laowang'

    def set_bar(self, value):
        """必须两个参数"""
        print("setter...")
        return 'set value' + value

    def del_bar(self):
        print("deleter...")

    BAR = property(get_bar, set_bar, del_bar, "description...")

obj = Foo()

obj.BAR  # 自动调用第一个参数中定义的方法：get_bar
obj.BAR = "alex" # 自动调用第二个参数中定义的方法：set_bar