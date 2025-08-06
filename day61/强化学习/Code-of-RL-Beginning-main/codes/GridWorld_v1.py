# 导入numpy库，用于处理数组和矩阵
import numpy as np
# 导入random库，用于生成随机数
import random


class GridWorld_v1(object):
    # 初版gridworld，没有写trajectory逻辑以及，policy维度仅为1*25，
    # 目的是用来计算非stochastic情况下policy iteration和value iteration 的贝尔曼方程解

    # n行，m列，随机若干个forbiddenArea，随机若干个target
    # A1: move upwards
    # A2: move rightwards;
    # A3: move downwards;
    # A4: move leftwards;
    # A5: stay unchanged;

    # 大小为rows*columns的list，每个位置存的是state的编号
    stateMap = None  
    # 大小为rows*columns的list，每个位置存的是奖励值 0 1 -10
    scoreMap = None  
    # targetArea的得分
    score = 0  
    # forbiddenArea的得分
    forbiddenAreaScore = 0  

    def __init__(self, rows=4, columns=5, forbiddenAreaNums=3, targetNums=1, seed=-1, score=1, forbiddenAreaScore=-1, 
                 desc=None): 
        # 1、构造函数（构造一个自定义or随机的网格世界）
        # 设置目标区域的得分
        self.score = score
        # 设置禁止区域的得分
        self.forbiddenAreaScore = forbiddenAreaScore
        if (desc != None):
            # if the gridWorld is fixed
            # 获取网格世界的行数
            self.rows = len(desc)
            # 获取网格世界的列数
            self.columns = len(desc[0])
            # 用于存储得分的临时列表
            l = []
            for i in range(self.rows):
                # 每行的得分列表
                tmp = []
                for j in range(self.columns):
                    # 根据描述设置每个位置的得分，'#'表示禁止区域，'T'表示目标区域，其他位置得分为0
                    tmp.append(forbiddenAreaScore if desc[i][j] == '#' else score if desc[i][j] == 'T' else 0)
                l.append(tmp)
            # 将得分列表转换为numpy数组
            self.scoreMap = np.array(l)
            # 生成状态映射表，每个位置的状态编号为行索引乘以列数加上列索引
            self.stateMap = [[i * self.columns + j for j in range(self.columns)] for i in range(self.rows)]
            return

        # if the gridWorld is random
        # 设置网格世界的行数
        self.rows = rows
        # 设置网格世界的列数
        self.columns = columns
        # 设置禁止区域的数量
        self.forbiddenAreaNums = forbiddenAreaNums
        # 设置目标区域的数量
        self.targetNums = targetNums
        # 设置随机数种子
        self.seed = seed

        # 设置随机数种子
        random.seed(self.seed)
        # 生成从0到rows*columns-1的列表
        l = [i for i in range(self.rows * self.columns)]
        # 随机打乱列表顺序，目的是随机生成禁止区域和目标区域的位置
        random.shuffle(l)  # 用shuffle来重排列
        # 初始化得分列表
        self.g = [0 for i in range(self.rows * self.columns)]
        # 设置禁止进入的区域得分
        for i in range(forbiddenAreaNums):
            self.g[l[i]] = forbiddenAreaScore;  # 设置禁止进入的区域，惩罚为1
        # 设置目标区域得分
        for i in range(targetNums):
            self.g[l[forbiddenAreaNums + i]] = score  # 奖励值为1的targetArea

        # 将得分列表转换为numpy数组并调整形状
        self.scoreMap = np.array(self.g).reshape(rows, columns)
        # 生成状态映射表，是一个二维列表
        self.stateMap = [[i * self.columns + j for j in range(self.columns)] for i in range(self.rows)]

    def show(self):
        # 2、把网格世界展示出来（show函数）
        for i in range(self.rows):
            # 用于存储每行的可视化字符串
            s = ""
            for j in range(self.columns):
                # 根据得分选择对应的表情符号
                tmp = {0: "⬜️", self.forbiddenAreaScore: "🚫", self.score: "✅"}  
                s = s + tmp[self.scoreMap[i][j]]  # 选择对应的表情符号
            # 打印每行的可视化字符串
            print(s)

    # 5*5
    def getScore(self, nowState, action):
        # 3、在当前状态[0,24]，执行动作[0,4]的得分及下一个状态
        # 计算当前状态的行坐标
        nowx = nowState // self.columns
        # 计算当前状态的列坐标
        nowy = nowState % self.columns

        if (nowx < 0 or nowy < 0 or nowx >= self.rows or nowy >= self.columns):
            # 打印坐标错误信息
            print(f"coordinate error: ({nowx},{nowy})")
        if (action < 0 or action >= 5):
            # 打印动作错误信息
            print(f"action error: ({action})")

        # 上右下左 不动
        # 定义动作对应的坐标变化列表
        actionList = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)] 
        # 计算下一个位置的行坐标
        tmpx = nowx + actionList[action][0] #x是纵轴
        # 计算下一个位置的列坐标
        tmpy = nowy + actionList[action][1] #y是横轴
        # print(tmpx,tmpy)
        if (tmpx < 0 or tmpy < 0 or tmpx >= self.rows or tmpy >= self.columns):
            # 如果下一个位置超出边界，返回-1和当前状态
            return -1, nowState
        # 返回下一个位置的得分和状态
        return self.scoreMap[tmpx][tmpy], self.stateMap[tmpx][tmpy] # 这里的stateMap是二维列表，所以需要用[tmpx][tmpy]来获取状态编号

    def showPolicy(self, policy):
        # 4、把传递进来的policy参数，进行可视化展示
        # 用emoji表情，可视化策略，在平常的可通过区域就用普通箭头⬆️➡️⬇️⬅️
        # 但若是forbiddenArea，那就十万火急急急,于是变成了双箭头⏫️︎⏩️⏬⏪
        # 获取网格世界的行数
        rows = self.rows
        # 获取网格世界的列数
        columns = self.columns
        # 用于存储每行的可视化字符串
        s = ""
        for i in range(self.rows * self.columns):
            # 计算当前位置的行坐标
            nowx = i // columns
            # 计算当前位置的列坐标
            nowy = i % columns
            if (self.scoreMap[nowx][nowy] == self.score):
                # 如果当前位置是目标区域，添加✅
                s = s + "✅"
            if (self.scoreMap[nowx][nowy] == 0):
                # 如果当前位置是普通区域，根据策略添加对应的箭头
                tmp = {0: "⬆️", 1: "➡️", 2: "⬇️", 3: "⬅️", 4: "🔄"}
                s = s + tmp[policy[i]]
            if (self.scoreMap[nowx][nowy] == self.forbiddenAreaScore):
                # 如果当前位置是禁止区域，根据策略添加对应的双箭头
                tmp = {0: "⏫️", 1: "⏩️", 2: "⏬", 3: "⏪", 4: "🔄"}
                s = s + tmp[policy[i]]
            if (nowy == columns - 1):
                # 如果到达行末，打印当前行的可视化字符串并清空
                print(s)
                s = ""
