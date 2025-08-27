# 作者: 王道 龙哥
# 2025年08月26日09时32分53秒
# xxx@qq.com
class File:
    def __init__(self, file_name, mode):
        """
        初始化File类
        :param file_name: 文件名
        :param mode: 打开模式，如'r', 'w', 'a'等
        """
        self.file_name = file_name
        self.mode = mode
        self.file = None

    def __enter__(self):
        """
        上下文管理器的进入方法，在with语句开始时被调用
        :return: 打开的文件对象
        """
        print(f"打开文件: {self.file_name}, 模式: {self.mode}")
        self.file = open(self.file_name, self.mode)
        return self.file #被f得到

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器的退出方法，在with语句结束时被调用
        :param exc_type: 异常类型
        :param exc_val: 异常值
        :param exc_tb: 异常追踪信息
        :return: None
        """
        if self.file:
            self.file.close()
            print(f"关闭文件: {self.file_name}")
        
        # 如果有异常发生，打印异常信息
        if exc_type:
            print(f"发生异常: {exc_type}, {exc_val}")
        
        # 返回False表示不抑制异常，如果有异常会继续向外传播
        # 返回True则会抑制异常
        return False


# 使用示例
if __name__ == "__main__":
    # 写入文件
    with File("test.txt", "w") as f:
        f.write("这是一个测试文件\n")
        f.write("使用自定义的File类实现with上下文管理器\n")
    
    # # 读取文件
    # with File("test.txt", "r") as f:
    #     content = f.read()
    #     print("文件内容:")
    #     print(content)
