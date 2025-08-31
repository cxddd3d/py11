# 作者: 王道 龙哥
# 2025年08月30日11时17分30秒
# xxx@qq.com
from abc import abstractmethod, ABCMeta


class Walk_animal(metaclass=ABCMeta):
    @abstractmethod
    def walk(self):
        print('walk')


class Swim_animal(metaclass=ABCMeta):
    @abstractmethod
    def swim(self): pass


class Fly_animal(metaclass=ABCMeta):
    @abstractmethod
    def fly(self): pass


# 如果正常一个老虎有跑和跑的方法的话，我们会这么做
# class Tiger:
#     def walk(self):
#         pass
#
#     def swim(self):
#         pass


# 但是我们使用接口类多继承的话就简单多了，并且规范了相同功能
class Tiger(Walk_animal, Swim_animal):
    def walk(self):
            pass

    def swim(self):
            pass


# # 如果此时再有一个天鹅swan,会飞，走，游泳 那么我们这么做
# class Swan(Walk_animal, Swim_animal, Fly_animal): pass
tiger = Tiger()