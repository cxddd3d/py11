# 作者: 王道 龙哥
# 2025年08月25日15时09分28秒
# xxx@qq.com
print("******多继承使用类名.__init__ 发生的状态******")


class Parent(object):
    def __init__(self, name):
        print('parent的init开始被调用')
        self.name = name
        print('parent的init结束被调用')


class Son1(Parent):
    def __init__(self, name, age,*args,**kwargs):  # *args,**kwargs 是为了接收Son2的参数
        print('Son1的init开始被调用')
        self.age = age
        super().__init__(name,*args,**kwargs) #*args,**kwargs 是为了接收Son2的参数
        print('Son1的init结束被调用')


class Son2(Parent):
    def __init__(self, name, gender,*args,**kwargs):  # *args,**kwargs 是为了接收Grandson的参数
        print('Son2的init开始被调用')
        self.gender=gender
        super().__init__(name)
        print('Son2的init结束被调用')


class Grandson(Son1, Son2):
    def __init__(self, name, age, gender,height):
        print('Grandson的init开始被调用')
        self.height=height
        super().__init__(name,age,gender)
        print('Grandson的init结束被调用')

print(Grandson.__mro__)
gs = Grandson('grandson', 12, '男',175)
print('姓名：', gs.name)
print('年龄：', gs.age)
print('性别：', gs.gender)
print('身高：',gs.height)
print("******多继承使用类名.__init__ 发生的状态******\n\n")
