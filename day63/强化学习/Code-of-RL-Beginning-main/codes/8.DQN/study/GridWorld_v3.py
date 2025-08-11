import numpy as np
import random
# 跟v1版本的区别主要是两点，v1是针对deterministic(确定性)的策略的，v2是针对stochastic的策略的，
# 具体来说的话就是，v2版本支持在同一个state概率选择若干个动作
# 它的策略矩阵，现在是 shape==(25,5)的第一维表示state，第二维表示action，返回一个概率
# 在打印策略的时候，将把每个state最大概率的动作打印出来
#
# 第二点区别是，在v2版本里面，引入了trajectory的概念
# 通过getTrajectoryScore方法可以直接按照提供的policy，进行采样若干步

# v3是最终版本，它引入了是否终止的概念，在trajectory里面每一步都有一个是否终止的标志。terminate表示是否终止,这样不需要像v2版本。v2版本
#里有一个stop_when_reach_target的参数，如果为True，则当到达目标区域时停止采样，如果为False，则一直采样直到采样steps步，如果为True，
# 则采样20000步，这样可以保证一定能到达目标区域


class GridWorld_v3(object): 
    """
    表示一个GridWorld的环境类，支持随机和固定两种方式初始化网格世界。

    Attributes:
        stateMap (list): 大小为rows*columns的二维列表，每个位置存储状态编号。
        scoreMap (numpy.ndarray): 大小为rows*columns的二维数组，每个位置存储奖励值，值为 0、1 或 -1。
        score (int): 目标区域的得分。
        forbiddenAreaScore (int): 禁止区域的得分。
        rows (int): 网格的行数。
        columns (int): 网格的列数。
        forbiddenAreaNums (int): 禁止区域的数量。
        targetNums (int): 目标区域的数量。
        seed (int): 随机数种子。
    """
    # 大小为rows*columns的list，每个位置存的是state的编号
    stateMap = None  
    # 大小为rows*columns的list，每个位置存的是奖励值 0 1 -1
    scoreMap = None  
    # targetArea的得分
    score = 0             
    # forbiddenArea的得分
    forbiddenAreaScore = 0  

    def __init__(self, rows=4, columns=5, forbiddenAreaNums=3, targetNums=1, seed=-1, score=1, forbiddenAreaScore=-1, desc=None):
        """
        初始化GridWorld_v3类的实例。

        Args:
            rows (int, optional): 网格的行数。默认为 4。
            columns (int, optional): 网格的列数。默认为 5。
            forbiddenAreaNums (int, optional): 禁止区域的数量。默认为 3。
            targetNums (int, optional): 目标区域的数量。默认为 1。
            seed (int, optional): 随机数种子。默认为 -1。
            score (int, optional): 目标区域的得分。默认为 1。
            forbiddenAreaScore (int, optional): 禁止区域的得分。默认为 -1。
            desc (list, optional): 用于固定网格世界的二维列表。默认为 None。
        """
        self.score = score
        self.forbiddenAreaScore = forbiddenAreaScore
        if desc is not None:
            # if the gridWorld is fixed
            self.rows = len(desc)
            self.columns = len(desc[0])
            l = []
            for i in range(self.rows):
                tmp = []
                for j in range(self.columns):
                    # 根据描述设置每个位置的奖励值
                    tmp.append(forbiddenAreaScore if desc[i][j] == '#' else score if desc[i][j] == 'T' else 0)
                l.append(tmp)
            self.scoreMap = np.array(l)
            # 初始化状态映射表
            self.stateMap = [[i * self.columns + j for j in range(self.columns)] for i in range(self.rows)]
            return

        # if the gridWorld is random
        self.rows = rows
        self.columns = columns
        self.forbiddenAreaNums = forbiddenAreaNums
        self.targetNums = targetNums
        self.seed = seed

        random.seed(self.seed)
        # 生成所有状态的列表
        l = [i for i in range(self.rows * self.columns)]
        # 用shuffle来重排列
        random.shuffle(l)  
        self.g = [0 for i in range(self.rows * self.columns)]
        for i in range(forbiddenAreaNums):
            # 设置禁止进入的区域，惩罚为forbiddenAreaScore
            self.g[l[i]] = forbiddenAreaScore  
        for i in range(targetNums):
            # 奖励值为score的targetArea
            self.g[l[forbiddenAreaNums + i]] = score  
            
        self.scoreMap = np.array(self.g).reshape(rows, columns)
        # 初始化状态映射表
        self.stateMap = [[i * self.columns + j for j in range(self.columns)] for i in range(self.rows)]

    def show(self):
        """
        可视化网格世界，用表情符号表示不同类型的区域。
        """
        for i in range(self.rows):
            s = ""
            for j in range(self.columns):
                tmp = {0: "⬜️", self.forbiddenAreaScore: "🚫", self.score: "✅"}
                s = s + tmp[self.scoreMap[i][j]]
            print(s)

    def getScore(self, nowState, action):
        """
        根据当前状态和动作，计算奖励并返回下一个状态。

        Args:
            nowState (int): 当前状态的编号。
            action (int): 采取的动作编号，范围从 0 到 4。

        Returns:
            tuple: 包含奖励值和下一个状态编号的元组。如果越界，奖励值为 -1，下一个状态为当前状态。
        """
        # 计算当前状态的坐标
        nowx = nowState // self.columns
        nowy = nowState % self.columns

        if nowx < 0 or nowy < 0 or nowx >= self.rows or nowy >= self.columns:
            print(f"coordinate error: ({nowx},{nowy})")
        if action < 0 or action >= 5:
            print(f"action error: ({action})")

        # 上右下左 不动
        actionList = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]
        tmpx = nowx + actionList[action][0]
        tmpy = nowy + actionList[action][1]
        # print(tmpx,tmpy)
        if tmpx < 0 or tmpy < 0 or tmpx >= self.rows or tmpy >= self.columns:
            return -1, nowState
        return self.scoreMap[tmpx][tmpy], self.stateMap[tmpx][tmpy]

    def getTrajectoryScore(self, nowState, action, policy):
        """
        根据给定的策略，从当前状态和动作开始采样轨迹，并计算轨迹得分。

        Args:
            nowState (int): 当前状态的编号。
            action (int): 初始动作的编号。
            policy (list): 一个 (rows*columns) * actions 的二维列表，其中每一行的总和为 1，
                           代表每个状态选择五个动作的概率总和为 1。

        Returns:
            list: 一个包含轨迹信息的列表，每个元素是一个元组 (nowState, nowAction, score, nextState, nextAction, terminal)。
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
            # 根据策略随机选择下一个动作
            nextAction = np.random.choice(range(5), size=1, replace=False, p=policy[nextState])[0]

            terminal = 0
            # 计算下一个状态的坐标
            nxtx, nxty = nextState // self.columns, nextState % self.columns
            if self.scoreMap[nxtx][nxty] == self.score:
                terminal = 1

            res.append((nowState, nowAction, score, nextState, nextAction, terminal))

            if terminal:# 当到达目标区域时停止采样
                return res
        return res

    def showPolicy(self, policy):
        """
        可视化给定的策略，用表情符号表示每个状态下的最优动作。

        Args:
            policy (list): 一个 (rows*columns) * actions 的二维列表，代表每个状态选择五个动作的概率。
        """
        # 用emoji表情，可视化策略，在平常的可通过区域就用普通箭头⬆️➡️⬇️⬅️
        # 但若是forbiddenArea，那就十万火急急急,于是变成了双箭头⏫︎⏩️⏬⏪
        rows = self.rows
        columns = self.columns
        s = ""
        # print(policy)
        for i in range(self.rows * self.columns):
            nowx = i // columns
            nowy = i % columns
            if self.scoreMap[nowx][nowy] == self.score:
                s = s + "✅"
            if self.scoreMap[nowx][nowy] == 0:
                tmp = {0: "⬆️", 1: "➡️", 2: "⬇️", 3: "⬅️", 4: "🔄"}
                # 选择概率最大的动作对应的箭头
                s = s + tmp[np.argmax(policy[i])]
            if self.scoreMap[nowx][nowy] == self.forbiddenAreaScore:
                tmp = {0: "⏫️", 1: "⏩️", 2: "⏬", 3: "⏪", 4: "🔄"}
                # 选择概率最大的动作对应的双箭头
                s = s + tmp[np.argmax(policy[i])]
            if nowy == columns - 1:
                print(s)
                s = ""