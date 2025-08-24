# 作者: 王道 龙哥
# 2025年08月23日09时42分32秒
# xxx@qq.com
def gen():
    i = 0
    while i < 5:
        temp=yield i
        print(temp)
        i += 1


G = gen()
print(next(G))
print(G.send('haha'))
