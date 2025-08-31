# 作者: 王道 龙哥
# 2025年08月28日16时38分12秒
# xxx@qq.com
def line6(k, b):
    def create_y(x):
        print(k * x + b)

    return create_y


line6_5_1 = line6(5, 1)
line6_6_2 = line6(6, 2)
line6_5_1(1)
line6_5_1(2)

line6_6_2(1)
line6_6_2(2)
