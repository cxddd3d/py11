# 作者: 王道 龙哥
# 2025年08月29日10时28分36秒
# xxx@qq.com
import time

def timing_decorator(func):
   def wrapper(*args, **kwargs):
      start_time = time.time()
      result = func(*args, **kwargs)
      end_time = time.time()
      print(f"{func.__name__} 函数执行时间: {end_time - start_time:.6f} 秒")
      return result
   return wrapper

@timing_decorator
def test1():
   print("-----test1----")
   for i in range(1000000):
      pass


test1()