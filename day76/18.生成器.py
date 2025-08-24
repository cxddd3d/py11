def fibonacci_generator(n):
    """
    斐波那契数列生成器
    :param n: 生成斐波那契数列的个数
    :return: 依次返回斐波那契数列中的每个数
    """
    a, b = 0, 1  # 初始化前两个数
    count = 0
    
    while count < n:
        yield a  # 生成当前的斐波那契数
        a, b = b, a + b  # 计算下一个斐波那契数
        count += 1


# 使用生成器生成斐波那契数列
if __name__ == "__main__":
    # 生成前10个斐波那契数
    fib = fibonacci_generator(10)
    
    print("斐波那契数列前10个数:")
    for num in fib:
        print(num, end=" ")
    
    # 另一种使用方式
    print("\n\n使用next()函数获取斐波那契数列:")
    fib_gen = fibonacci_generator(5)
    print(fib_gen)
