import numpy as np
import random
# 跟v1版本的区别主要是两点，v1是针对deteministic的策略的，v2是针对stochastic的策略的，
# 具体来说的话就是，v2版本支持在同一个state概率选择若干个动作
# 它的策略矩阵，现在是 shape==(25,5)的第一维表示state，第二维表示action，返回一个概率
# 在打印策略的时候，将把每个state最大概率的动作打印出来
#
# 第二点区别是，在v2版本里面，引入了trajectory的概念
# 通过getTrajectoryScore方法可以直接按照提供的policy，进行采样若干步

# v3是最终版本，它引入了是否终止的概念，在trajectory里面每一步都有一个是否终止的标志。
# 此外v3的最后一步，不再是以target state为起点，而是以target state为终点。也就是trajectory比v2版本会少了一步

# v4是v3的GYM版本，它向下兼容v3，但是增加了step+reset功能
# step就是往前用action推演一步
# reset就是把状态重置了并返回当前的state

# v5版本进行了两个改进，一个是把state改成了(x,y)行列的形式，另一个是把v5拆成了两个环境，一个环境是可以stay的，一个环境是不可以stay的，主要通过action shape=4或者=5进行替换
# 另外，把bug进行了修复，并且增加了一个返回地图的API,无需管这段备注

class GridWorld_v5(object):
    """
    GridWorld_v5 类用于创建一个网格世界环境，支持多种配置和操作。

    属性:
        stateMap (list): 大小为 rows*columns 的二维列表，每个位置存储状态编号。
        scoreMap (np.ndarray): 大小为 rows*columns 的二维数组，每个位置存储奖励值（0, 1, -1）。
        score (int): 目标区域的得分。
        forbiddenAreaScore (int): 禁止区域的得分。
        moveScore (int): 移动得分。
        hitWallScore (int): 撞墙得分。
        terminal (int): 表示是否终止的标志。
        action_space (int): 动作空间的大小。
        map_description (list): 地图的描述信息。
        rows (int): 网格的行数。
        columns (int): 网格的列数。
        initState (list): 初始状态。
        nowState (list): 当前状态。
    """
    stateMap = None  # 大小为rows*columns的list，每个位置存的是state的编号
    scoreMap = None  # 大小为rows*columns的list，每个位置存的是奖励值 0 1 -1
    score = 0  # targetArea的得分
    forbiddenAreaScore = 0  # forbiddenArea的得分

    def __init__(self, initState=10, rows=4, columns=5, forbiddenAreaNums=3, targetNums=1, seed=-1, score=1, 
                 forbiddenAreaScore=-1, hitWallScore=-1, moveScore = 0, action_space = 5, desc=None):
        """
        初始化 GridWorld_v5 环境。

        参数:
            initState (int): 初始状态的编号，默认为 10。
            rows (int): 网格的行数，默认为 4。
            columns (int): 网格的列数，默认为 5。
            forbiddenAreaNums (int): 禁止区域的数量，默认为 3。
            targetNums (int): 目标区域的数量，默认为 1。
            seed (int): 随机数种子，默认为 -1。
            score (int): 目标区域的得分，默认为 1。
            forbiddenAreaScore (int): 禁止区域的得分，默认为 -1。
            hitWallScore (int): 撞墙的得分，默认为 -1。
            moveScore (int): 移动的得分，默认为 0。
            action_space (int): 动作空间的大小，默认为 5。
            desc (list): 地图的描述信息，默认为 None。
        """
        self.moveScore = moveScore
        self.score = score
        self.forbiddenAreaScore = forbiddenAreaScore
        self.hitWallScore = hitWallScore
        self.terminal = 0
        self.action_space = action_space
        self.map_description = None

        if (desc != None):
            # if the gridWorld is fixed
            self.map_description = desc
            self.rows = len(desc)
            self.columns = len(desc[0])
            self.initState = [initState // self.columns, initState % self.columns]
            self.nowState = self.initState
            l = []
            for i in range(self.rows):
                tmp = []
                for j in range(self.columns):
                    # 根据地图描述设置奖励值
                    tmp.append(forbiddenAreaScore if desc[i][j] == '#' else score if desc[i][j] == 'T' else self.moveScore)
                l.append(tmp)
            self.scoreMap = np.array(l)
            self.stateMap = [[i * self.columns + j for j in range(self.columns)] for i in range(self.rows)]
            return

        # if the gridWorld is random
        self.rows = rows
        self.columns = columns
        self.forbiddenAreaNums = forbiddenAreaNums
        self.targetNums = targetNums
        self.seed = seed

        random.seed(self.seed)
        l = [i for i in range(self.rows * self.columns)]
        random.shuffle(l)  # 用shuffle来重排列
        self.g = [self.moveScore for i in range(self.rows * self.columns)]
        for i in range(forbiddenAreaNums):
            self.g[l[i]] = forbiddenAreaScore  # 设置禁止进入的区域，惩罚为1
        for i in range(targetNums):
            self.g[l[forbiddenAreaNums + i]] = score  # 奖励值为1的targetArea

        self.scoreMap = np.array(self.g).reshape(rows, columns)
        desc = []
        for i in range(self.rows):
            s = ""
            for j in range(self.columns):
                tmp = {self.moveScore: ".", self.forbiddenAreaScore: "#", self.score: "T"}
                s = s + tmp[self.scoreMap[i][j]]
            desc.append(s)
        self.map_description = desc # 这个是地图的描述信息
        self.stateMap = [[i * self.columns + j for j in range(self.columns)] for i in range(self.rows)]

    def get_observation_space(self):
        """
        获取观察空间的维度。

        返回:
            int: 观察空间的维度，固定为 2。
        """
        return 2

    def get_action_space(self):
        """
        获取动作空间的大小。

        返回:
            int: 动作空间的大小。
        """
        return self.action_space

    def get_map_description(self):
        """
        获取地图的描述信息。

        返回:
            list: 地图的描述信息。
        """
        return self.map_description
        
    def show(self):
        """
        打印网格世界的可视化表示。
        """
        for i in range(self.rows):
            s = ""
            for j in range(self.columns):
                tmp = {self.moveScore: "⬜️", self.forbiddenAreaScore: "🚫", self.score: "✅"}
                s = s + tmp[self.scoreMap[i][j]]
            print(s)

    def getScore(self, nowState, action):
        """
        根据当前状态和动作计算得分，并返回下一个状态。

        参数:
            nowState (int): 当前状态的编号。
            action (int): 执行的动作编号。

        返回:
            tuple: 包含得分和下一个状态编号的元组。
        """
        nowx = nowState // self.columns
        nowy = nowState % self.columns

        if (nowx < 0 or nowy < 0 or nowx >= self.rows or nowy >= self.columns):
            print(f"coordinate error: ({nowx},{nowy})")
        if (action < 0 or action >= self.action_space):
            print(f"action error: ({action})")

        # 上右下左 不动
        actionList = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]
        tmpx = nowx + actionList[action][0]
        tmpy = nowy + actionList[action][1]
        # print(tmpx,tmpy)
        if (tmpx < 0 or tmpy < 0 or tmpx >= self.rows or tmpy >= self.columns):
            return self.hitWallScore, nowState
        return self.scoreMap[tmpx][tmpy], self.stateMap[tmpx][tmpy]

    def getTrajectoryScore(self, nowState, action, policy):
        """
        根据提供的策略采样轨迹并计算得分。

        参数:
            nowState (int): 当前状态的编号。
            action (int): 初始动作的编号。
            policy (list): 二维列表，表示每个状态下选择动作的概率分布。

        返回:
            list: 包含轨迹信息的列表，每个元素是一个元组 (nowState, nowAction, score, nextState, nextAction, terminal)。
        """
        # policy是一个 (rows*columns) * actions的二维列表，其中每一行的总和为1，代表每个state选择五个action的概率总和为1
        # Attention: 返回值是一个大小为steps+1的列表，因为第一步也计算在里面了
        # 其中的元素是(nowState, nowAction, score, nextState, nextAction, terminal)元组

        res = []
        nextState = nowState
        nextAction = action

        for i in range(1001):
            nowState = nextState
            nowAction = nextAction

            score, nextState = self.getScore(nowState, nowAction)
            nextAction = np.random.choice(range(self.action_space), size=1, replace=False, p=policy[nextState])[0]

            terminal = 0
            nxtx, nxty = nextState // self.columns, nextState % self.columns
            if self.scoreMap[nxtx][nxty] == self.score:
                terminal = 1

            res.append((nowState, nowAction, score, nextState, nextAction, terminal))

            if terminal:
                return res
        return res

    def showPolicy(self, policy):
        """
        可视化策略，用表情符号表示每个状态下的最优动作。

        参数:
            policy (list): 二维列表，表示每个状态下选择动作的概率分布。
        """
        # 用emoji表情，可视化策略，在平常的可通过区域就用普通箭头⬆️➡️⬇️⬅️
        # 但若是forbiddenArea，那就十万火急急急,于是变成了双箭头⏫️⏩️⏬⏪
        rows = self.rows
        columns = self.columns
        s = ""
        # print(policy)
        for i in range(self.rows * self.columns):
            nowx = i // columns
            nowy = i % columns
            if (self.scoreMap[nowx][nowy] == self.score):
                s = s + "✅"
            if (self.scoreMap[nowx][nowy] == self.moveScore):
                tmp = {0: "⬆️", 1: "➡️", 2: "⬇️", 3: "⬅️", 4: "🔄"}
                s = s + tmp[np.argmax(policy[i])]
            if (self.scoreMap[nowx][nowy] == self.forbiddenAreaScore):
                tmp = {0: "⏫️", 1: "⏩️", 2: "⏬", 3: "⏪", 4: "🔄"}
                s = s + tmp[np.argmax(policy[i])]
            if (nowy == columns - 1):
                print(s)
                s = ""

    def reset(self):
        """
        重置环境状态并返回初始状态。

        返回:
            list: 初始状态的坐标。
        """
        self.nowState = self.initState
        self.terminal = 0
        return self.nowState

    def step(self,action):
        """
        根据给定的动作执行一步环境交互。

        参数:
            action (int): 执行的动作编号。

        返回:
            tuple: 包含下一个状态、得分、是否终止和额外信息的元组。
        """
        score, nextState = self.getScore(self.nowState[0]*self.columns+self.nowState[1], action)

        # self.nowState = nextState
        # terminal = 0
        nxtx, nxty = nextState // self.columns, nextState % self.columns
        nextState = [nxtx,nxty]
        self.nowState = [nxtx,nxty]
        if self.scoreMap[nxtx][nxty] == self.score:
            self.terminal = 1

        return nextState,score,self.terminal,0
