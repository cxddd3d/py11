import numpy as np  # 导入numpy库，用于数值计算
import random  # 导入random库，用于生成随机数
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
# 另外，把bug进行了修复，并且增加了一个返回地图的API

class GridWorld_v6(object):  # 定义GridWorld_v6类，继承自object
    # n行，m列，随机若干个forbiddenArea，随机若干个target
    # A1: move upwards
    # A2: move rightwards;
    # A3: move downwards;
    # A4: move leftwards;
    # A5: stay unchanged;

    stateMap = None  # 大小为rows*columns的list，每个位置存的是state的编号
    scoreMap = None  # 大小为rows*columns的list，每个位置存的是奖励值 0 1 -1
    score = 0  # targetArea的得分
    forbiddenAreaScore = 0  # forbiddenArea的得分

    def __init__(self, initState=10, rows=4, columns=5, forbiddenAreaNums=3, targetNums=1, seed=-1, score=1, 
                 forbiddenAreaScore=-1, hitWallScore=-1, moveScore = 0, action_space = 5, desc=None, enterForbiddenArea=True):  # 初始化方法，设置各种参数
        self.moveScore = moveScore  # 设置移动得分
        self.score = score  # 设置目标区域得分
        self.forbiddenAreaScore = forbiddenAreaScore  # 设置禁区得分
        self.hitWallScore = hitWallScore  # 设置撞墙得分
        self.terminal = 0  # 初始化终止状态为0
        self.action_space = action_space  # 设置动作空间大小
        self.map_description = None  # 初始化地图描述为None
        self.enterForbiddenArea = enterForbiddenArea  # 设置是否可以进入禁区

        if (desc != None):  # 如果提供了地图描述
            # if the gridWorld is fixed
            self.map_description = desc  # 设置地图描述
            self.rows = len(desc)  # 设置行数为描述的长度
            self.columns = len(desc[0])  # 设置列数为第一行描述的长度
            self.initState = [initState // self.columns, initState % self.columns]  # 计算初始状态的坐标
            self.nowState = self.initState  # 设置当前状态为初始状态
            l = []  # 创建空列表用于存储得分地图
            for i in range(self.rows):  # 遍历每一行
                tmp = []  # 创建临时列表存储当前行的得分
                for j in range(self.columns):  # 遍历每一列
                    tmp.append(forbiddenAreaScore if desc[i][j] == '#' else score if desc[i][j] == 'T' else self.moveScore)  # 根据地图描述设置得分
                l.append(tmp)  # 将当前行添加到得分地图
            self.scoreMap = np.array(l)  # 将得分地图转换为numpy数组
            self.stateMap = [[i * self.columns + j for j in range(self.columns)] for i in range(self.rows)]  # 创建状态映射
            return  # 返回，结束初始化

        # TODO: fix random 这里的不应该用得分来作为衡量，应该用map_description作为衡量
        # if the gridWorld is random
        self.rows = rows  # 设置行数
        self.columns = columns  # 设置列数
        self.forbiddenAreaNums = forbiddenAreaNums  # 设置禁区数量
        self.targetNums = targetNums  # 设置目标区域数量
        self.seed = seed  # 设置随机种子

        random.seed(self.seed)  # 使用种子初始化随机数生成器
        l = [i for i in range(self.rows * self.columns)]  # 创建包含所有状态编号的列表
        random.shuffle(l)  # 用shuffle来重排列
        self.g = [self.moveScore for i in range(self.rows * self.columns)]  # 初始化所有位置的得分为移动得分
        for i in range(forbiddenAreaNums):  # 遍历禁区数量
            self.g[l[i]] = forbiddenAreaScore  # 设置禁止进入的区域，惩罚为1
        for i in range(targetNums):  # 遍历目标区域数量
            self.g[l[forbiddenAreaNums + i]] = score  # 奖励值为1的targetArea

        self.scoreMap = np.array(self.g).reshape(rows, columns)  # 将得分列表重塑为二维数组
        desc = []  # 创建空列表用于存储地图描述
        for i in range(self.rows):  # 遍历每一行
            s = ""  # 创建空字符串
            for j in range(self.columns):  # 遍历每一列
                tmp = {self.moveScore: ".", self.forbiddenAreaScore: "#", self.score: "T"}  # 创建得分到字符的映射
                s = s + tmp[self.scoreMap[i][j]]  # 根据得分添加对应字符
            desc.append(s)  # 将当前行添加到地图描述
        self.map_description = desc  # 设置地图描述
        self.stateMap = [[i * self.columns + j for j in range(self.columns)] for i in range(self.rows)]  # 创建状态映射

    def get_observation_space(self):  # 获取观察空间大小的方法
        return 2  # 返回观察空间大小为2

    def get_action_space(self):  # 获取动作空间大小的方法
        return self.action_space  # 返回动作空间大小

    def get_map_description(self):  # 获取地图描述的方法
        return self.map_description  # 返回地图描述
        
    def show(self):  # 显示地图的方法
        for i in range(self.rows):  # 遍历每一行
            s = ""  # 创建空字符串
            for j in range(self.columns):  # 遍历每一列
                tmp = {'.': "⬜️", '#': "🚫", 'T': "✅"}  # 创建字符到表情的映射
                s = s + tmp[self.map_description[i][j]]  # 根据地图描述添加对应表情
            print(s)  # 打印当前行

    def getScore(self, nowState, action):  # 获取得分和下一状态的方法
        nowx = nowState // self.columns  # 计算当前状态的行坐标
        nowy = nowState % self.columns  # 计算当前状态的列坐标

        if (nowx < 0 or nowy < 0 or nowx >= self.rows or nowy >= self.columns):  # 如果坐标超出范围
            print(f"coordinate error: ({nowx},{nowy})")  # 打印坐标错误信息
        if (action < 0 or action >= self.action_space):  # 如果动作超出范围
            print(f"action error: ({action})")  # 打印动作错误信息

        # 上右下左 不动
        actionList = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]  # 定义动作对应的坐标变化
        tmpx = nowx + actionList[action][0]  # 计算执行动作后的行坐标
        tmpy = nowy + actionList[action][1]  # 计算执行动作后的列坐标
        # print(tmpx,tmpy)
        if (tmpx < 0 or tmpy < 0 or tmpx >= self.rows or tmpy >= self.columns):  # 如果新坐标超出范围
            return self.hitWallScore, nowState  # 返回撞墙得分和当前状态
        # if (tmpx < 0 or tmpy < 0 or tmpx >= self.rows or tmpy >= self.columns):
        #     return self.hitWallScore, nowState
        
        return self.scoreMap[tmpx][tmpy], self.stateMap[tmpx][tmpy]  # 返回新位置的得分和状态编号

    def getTrajectoryScore(self, nowState, action, policy):  # 获取轨迹得分的方法
        # policy是一个 (rows*columns) * actions的二维列表，其中每一行的总和为1，代表每个state选择五个action的概率总和为1
        # Attention: 返回值是一个大小为steps+1的列表，因为第一步也计算在里面了
        # 其中的元素是(nowState, nowAction, score, nextState, nextAction, terminal)元组

        res = []  # 创建空列表用于存储结果
        nextState = nowState  # 设置下一状态为当前状态
        nextAction = action  # 设置下一动作为当前动作

        for i in range(1001):  # 最多循环1001次
            nowState = nextState  # 更新当前状态
            nowAction = nextAction  # 更新当前动作

            score, nextState = self.getScore(nowState, nowAction)  # 获取得分和下一状态
            nextAction = np.random.choice(range(self.action_space), size=1, replace=False, p=policy[nextState])[0]  # 根据策略选择下一动作

            terminal = 0  # 初始化终止标志为0
            nxtx, nxty = nextState // self.columns, nextState % self.columns  # 计算下一状态的坐标
            if self.scoreMap[nxtx][nxty] == self.score:  # 如果下一状态是目标区域
                terminal = 1  # 设置终止标志为1

            res.append((nowState, nowAction, score, nextState, nextAction, terminal))  # 将当前步骤信息添加到结果

            if terminal:  # 如果到达终止状态
                return res  # 返回结果
        return res  # 返回结果

    def showPolicy(self, policy):  # 显示策略的方法
        # 用emoji表情，可视化策略，在平常的可通过区域就用普通箭头⬆️➡️⬇️⬅️
        # 但若是forbiddenArea，那就十万火急急急,于是变成了双箭头⏫️⏩️⏬⏪
        rows = self.rows  # 获取行数
        columns = self.columns  # 获取列数
        s = ""  # 创建空字符串
        # print(policy)
        for i in range(self.rows * self.columns):  # 遍历所有状态
            nowx = i // columns  # 计算当前状态的行坐标
            nowy = i % columns  # 计算当前状态的列坐标
            if (self.scoreMap[nowx][nowy] == self.score):  # 如果当前位置是目标区域
                s = s + "✅"  # 添加目标标志
            if (self.scoreMap[nowx][nowy] == self.moveScore):  # 如果当前位置是普通区域
                tmp = {0: "⬆️", 1: "➡️", 2: "⬇️", 3: "⬅️", 4: "🔄"}  # 创建动作到箭头的映射
                s = s + tmp[np.argmax(policy[i])]  # 添加最大概率动作对应的箭头
            if (self.scoreMap[nowx][nowy] == self.forbiddenAreaScore):  # 如果当前位置是禁区
                tmp = {0: "⏫️", 1: "⏩️", 2: "⏬", 3: "⏪", 4: "🔄"}  # 创建动作到双箭头的映射
                s = s + tmp[np.argmax(policy[i])]  # 添加最大概率动作对应的双箭头
            if (nowy == columns - 1):  # 如果到达行尾
                print(s)  # 打印当前行
                s = ""  # 重置字符串

    def reset(self):  # 重置环境的方法
        self.nowState = self.initState  # 将当前状态重置为初始状态
        self.terminal = 0  # 重置终止标志为0
        return self.nowState  # 返回当前状态

    def step(self,action):  # 执行一步动作的方法
        score, nextState = self.getScore(self.nowState[0]*self.columns+self.nowState[1], action)  # 获取得分和下一状态

        # self.nowState = nextState
        # terminal = 0
        nxtx, nxty = nextState // self.columns, nextState % self.columns  # 计算下一状态的坐标
        nextState = [nxtx,nxty]  # 将下一状态转换为坐标形式
        self.nowState = [nxtx,nxty]  # 更新当前状态
        if self.scoreMap[nxtx][nxty] == self.score:  # 如果下一状态是目标区域
            self.terminal = 1  # 设置终止标志为1

        if self.enterForbiddenArea == False and self.map_description[nxtx][nxty] == '#':  # 如果不允许进入禁区且下一状态是禁区
            self.terminal = 1  # 设置终止标志为1

        return nextState,score,self.terminal,0  # 返回下一状态、得分、终止标志和额外信息
