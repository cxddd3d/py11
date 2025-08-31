# 作者: 王道 龙哥
# 2025年08月28日16时37分30秒
# xxx@qq.com
class Line5:
    def __init__(self, k, b):
        self.k = k
        self.b = b

    def __call__(self, x):
        print(self.k * x + self.b)


line_5_1 = Line5(5, 1)
line_5_1(1)
line_5_1(2)
line_5_1(3)
print('-' * 50)
line_6_2 = Line5(6, 2)
line_6_2(1)
line_6_2(2)
line_6_2(3)


