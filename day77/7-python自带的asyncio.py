# 作者: 王道 龙哥
# 2025年08月23日
import asyncio
import random

async def work(n, count):
    """
    协程工作函数
    :param n: 协程编号
    :param count: 循环次数
    """
    for i in range(count):
        print(f"协程{n}执行第{i+1}次任务")
        # 模拟随机耗时操作
        sleep_time = random.uniform(0.05, 0.3)
        await asyncio.sleep(sleep_time)

async def main():
    # 创建3个协程任务
    count = 5  # 每个协程执行的循环次数
    tasks = [
        asyncio.create_task(work(1, count)),
        asyncio.create_task(work(2, count)),
        asyncio.create_task(work(3, count))
    ]
    
    # 等待所有协程执行完毕
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # 在Python 3.7+中可以直接使用asyncio.run()运行主协程
    asyncio.run(main())
