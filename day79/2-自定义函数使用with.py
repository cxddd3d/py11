# 作者: 王道 龙哥
# 2025年08月26日09时40分22秒
# xxx@qq.com
from contextlib import contextmanager

@contextmanager
def my_open(file_name, mode):
    print(f"打开文件: {file_name}, 模式: {mode}")
    f=open(file_name, mode) # 打开文件
    yield f # 返回文件对象,去执行with内的代码
    f.close() # 关闭文件
    print('关闭文件')

with my_open("test.txt", "w") as f:
    f.write("这是一个测试文件\n")