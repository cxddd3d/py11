from collections.abc import Iterable


class MyIterator(object):
    """
    当一个类中定义了__iter__和__next__方法，这个类就是迭代器类
    """
    def __init__(self, container):
        self.container = container
        self.index = 0

    def __iter__(self):
        """返回迭代器自身"""
        return self

    def __next__(self):
        """返回下一个元素，如果没有更多元素则抛出StopIteration异常"""
        if self.index < len(self.container):
            item = self.container[self.index] # 获取当前索引的元素
            self.index += 1 # 索引加1
            return item # 返回当前索引的元素
        else:
            # 迭代结束，抛出StopIteration异常
            raise StopIteration


class MyList(object):
    def __init__(self):
        self.container = []

    def add(self, item):
        self.container.append(item)

    def __iter__(self):
        """
        返回的是一个迭代器
        """
        return MyIterator(self.container)


my_list = MyList()
my_list.add(1)
my_list.add(2)
my_list.add(3)
print(isinstance(my_list, Iterable))

for i in my_list:
    print(i)

# list1 = [1,2,3,4,5]
# iter_list1=iter(list1)
# for i in iter_list1:
#     print(i)
# for i in iter_list1:
#     print(i)