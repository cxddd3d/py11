# 作者: 王道 龙哥
# 2025年08月28日16时44分53秒
# xxx@qq.com
x = 300


def test1(x):
    # x = 200

    def test2():
        # global x
        nonlocal x # 声明x是外部函数的变量
        print("----1----x=%d" % x)
        x = 100
        print("----2----x=%d" % x)

    return test2


t1 = test1(150)

t1()

print(f'全局变量x的值{x}')