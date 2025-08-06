import numpy as np
import random
# 跟v1版本的区别主要是两点，v1是针对deteministic的策略的，v2是针对stochastic的策略的，
# 具体来说的话就是，v2版本支持在同一个state概率选择若干个动作
# 它的策略矩阵，现在是 shape==(25,5)的第一维表示state，第二维表示action，返回一个概率
# 在打印策略的时候，将把每个state最大概率的动作打印出来
# 第二点区别是，在v2版本里面，引入了trajectory的概念
# 通过getTrajectoryScore方法可以直接按照提供的policy，进行采样若干步

class GridWorld_v2(object): 
    # n行，m列，随机若干个forbiddenArea，随机若干个target
    # A1: move upwards
    # A2: move rightwards;
    # A3: move downwards;
    # A4: move leftwards;
    # A5: stay unchanged;

    # 大小为rows*columns的list，每个位置存的是state的编号
    stateMap = None  
    # 大小为rows*columns的list，每个位置存的是奖励值 0 1 -1
    scoreMap = None  
    # targetArea的得分
    score = 0             
    # forbiddenArea的得分
    forbiddenAreaScore=0  

    def __init__(self,rows=4, columns=5, forbiddenAreaNums=3, targetNums=1, seed = -1, score = 1, forbiddenAreaScore = -1, desc=None):
        # 初始化目标区域得分
        self.score = score
        # 初始化禁止区域得分
        self.forbiddenAreaScore = forbiddenAreaScore
        if(desc != None):
            # if the gridWorld is fixed
            # 获取网格世界的行数
            self.rows = len(desc)
            # 获取网格世界的列数
            self.columns = len(desc[0])
            l = [] # 用于存储得分的列表
            for i in range(self.rows):
                tmp = []
                for j in range(self.columns):
                    # 根据描述设置每个位置的得分
                    tmp.append(forbiddenAreaScore if desc[i][j]=='#' else score if desc[i][j]=='T' else 0)
                l.append(tmp)
            # 将得分列表转换为numpy数组
            self.scoreMap = np.array(l)
            # 生成状态映射表
            self.stateMap = [[i*self.columns+j for j in range(self.columns)] for i in range(self.rows)]
            return
            
        # if the gridWorld is random
        # 初始化网格世界的行数
        self.rows = rows
        # 初始化网格世界的列数
        self.columns = columns
        # 初始化禁止区域的数量
        self.forbiddenAreaNums = forbiddenAreaNums
        # 初始化目标区域的数量
        self.targetNums = targetNums
        # 初始化随机数种子
        self.seed = seed

        # 设置随机数种子
        random.seed(self.seed)
        # 生成包含所有状态编号的列表
        l = [i for i in range(self.rows * self.columns)]
        # 用shuffle来重排列
        random.shuffle(l)  
        # 初始化得分列表
        self.g = [0 for i in range(self.rows * self.columns)]
        for i in range(forbiddenAreaNums):
            # 设置禁止进入的区域，惩罚为1
            self.g[l[i]] = forbiddenAreaScore
        for i in range(targetNums):
            # 奖励值为1的targetArea
            self.g[l[forbiddenAreaNums+i]] = score 
            
        # 将得分列表转换为numpy数组并调整形状
        self.scoreMap = np.array(self.g).reshape(rows,columns)
        # 生成状态映射表
        self.stateMap = [[i*self.columns+j for j in range(self.columns)] for i in range(self.rows)]

    def show(self):
        for i in range(self.rows):
            s = ""
            for j in range(self.columns):
                # 定义得分对应的表情符号
                tmp = {0:"⬜️",self.forbiddenAreaScore:"🚫",self.score:"✅"}
                # 拼接表情符号
                s = s + tmp[self.scoreMap[i][j]]
            print(s)
        
    def getScore(self, nowState, action):
        # 计算当前状态的行坐标
        nowx = nowState // self.columns
        # 计算当前状态的列坐标
        nowy = nowState % self.columns
        
        if(nowx<0 or nowy<0 or nowx>=self.rows or nowy>=self.columns):
            print(f"coordinate error: ({nowx},{nowy})")
        if(action<0 or action>=5 ):
            print(f"action error: ({action})")
            
        # 上右下左 不动
        actionList = [(-1,0),(0,1),(1,0),(0,-1),(0,0)]
        # 计算执行动作后的行坐标
        tmpx = nowx + actionList[action][0]
        # 计算执行动作后的列坐标
        tmpy = nowy + actionList[action][1]
        # print(tmpx,tmpy)
        if(tmpx<0 or tmpy<0 or tmpx>=self.rows or tmpy>=self.columns):
            return -1,nowState
        # 返回执行动作后的得分和下一个状态
        return self.scoreMap[tmpx][tmpy],self.stateMap[tmpx][tmpy]

    def getTrajectoryScore(self, nowState, action, policy, steps, stop_when_reach_target=False): #记录轨迹，与v1版本不同，这里的policy是一个 (rows*columns) * actions的二维列表，其中每一行的总和为1，代表每个state选择五个action的概率总和为1
        # policy是一个 (rows*columns) * actions的二维列表，其中每一行的总和为1，代表每个state选择五个action的概率总和为1
        # Attention: 返回值是一个大小为steps+1的列表，因为第一步也计算在里面了
        # 其中的元素是(nowState, nowAction, score, nextState, nextAction)元组
        
        # 初始化结果列表
        res = []
        # 初始化下一个状态
        nextState = nowState
        # 初始化下一个动作
        nextAction = action
        if stop_when_reach_target == True:# 当到达目标区域时停止采样，如果为False，则一直采样直到采样steps步，如果为True，则采样20000步，这样可以保证一定能到达目标区域
            steps = 20000
        for i in range(steps+1):
            # 更新当前状态
            nowState = nextState
            # 更新当前动作
            nowAction = nextAction

            # 获取执行动作后的得分和下一个状态
            score, nextState = self.getScore(nowState, nowAction)
            # 根据策略随机选择下一个动作，policy[nextState]是一个大小为5的列表，代表每个action的概率，概率总和为1，概率越大的action被选中的可能性越高
            #p是要传入的概率列表，replace=False表示不放回抽样
            nextAction = np.random.choice(range(5), size=1, replace=False, p=policy[nextState])[0] 

            # 将当前状态、动作、得分、下一个状态和下一个动作添加到结果列表中
            res.append((nowState, nowAction, score, nextState, nextAction))

            if (stop_when_reach_target):
                # print(nextState)
                # print(self.scoreMap)
                # 计算当前状态的行坐标
                nowx = nowState // self.columns
                # 计算当前状态的列坐标
                nowy = nowState % self.columns
                if self.scoreMap[nowx][nowy] == self.score: # 到达目标区域，停止采样
                    return res
        return res

    def showPolicy(self, policy):
        # 用emoji表情，可视化策略，在平常的可通过区域就用普通箭头⬆️➡️⬇️⬅️
        # 但若是forbiddenArea，那就十万火急急急,于是变成了双箭头⏫︎⏩️⏬⏪
        # 获取网格世界的行数
        rows = self.rows
        # 获取网格世界的列数
        columns = self.columns
        s = ""
        # print(policy)
        for i in range(self.rows * self.columns):
            # 计算当前状态的行坐标
            nowx = i // columns
            # 计算当前状态的列坐标
            nowy = i % columns
            if(self.scoreMap[nowx][nowy]==self.score):
                s = s + "✅"
            if(self.scoreMap[nowx][nowy]==0):
                # 定义普通区域动作对应的表情符号
                tmp = {0:"⬆️",1:"➡️",2:"⬇️",3:"⬅️",4:"🔄"}
                s = s + tmp[np.argmax(policy[i])]
            if(self.scoreMap[nowx][nowy]==self.forbiddenAreaScore):
                # 定义禁止区域动作对应的表情符号
                tmp = {0:"⏫️",1:"⏩️",2:"⏬",3:"⏪",4:"🔄"}
                s = s + tmp[np.argmax(policy[i])]
            if(nowy == columns-1):
                print(s)
                s = ""