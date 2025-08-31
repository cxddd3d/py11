# 作者: 王道 龙哥
# 2025年08月29日10时49分31秒
# xxx@qq.com

class Test:
    def __init__(self, func):
        print("初始化装饰器")
        self.func = func
    
    def __call__(self, *args, **kwargs):
        print("装饰器中的功能")
        return self.func(*args, **kwargs)



@Test
def hello():
    print("hello world")


# hello=Test(hello)

hello()  # 调用函数

import torch

torch.no_grad()