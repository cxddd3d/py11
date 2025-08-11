# 导入random模块，用于随机采样操作
import random
# 导入numpy模块，用于处理数组数据
import numpy as np

class ExperienceReplayBuffer():
    """
    经验回放缓冲区类，用于存储和采样智能体的经验数据。

    属性:
        max_size (int): 缓冲区的最大容量。
        buffer (list): 存储经验数据的列表。
    """
    def __init__(self, max_size):
        """
        初始化经验回放缓冲区。

        参数:
            max_size (int): 缓冲区的最大容量。
        """
        self.max_size = max_size
        # 初始化一个空列表用于存储经验数据
        self.buffer = []

    def getSize(self):
        """
        获取当前缓冲区中经验数据的数量。

        返回:
            int: 缓冲区中经验数据的数量。
        """
        return len(self.buffer)
        
    def add_expericence(self, experience):
        """
        向缓冲区中添加一条经验数据。如果缓冲区已满，则移除最早添加的数据。

        参数:
            experience (tuple): 一条经验数据，包含状态、动作、奖励、下一个状态、下一个动作和终止标志。
        """
        # state, action, reward, next_state, next_action, terminal
        if len(self.buffer) >= self.max_size:
            # 如果缓冲区已满，移除最早添加的经验数据，像一个队列，先进先出
            self.buffer.pop(0)
        # 将新的经验数据添加到缓冲区末尾
        self.buffer.append(experience)

    def sample_batch(self, batch_size):
        """
        从缓冲区中随机采样指定数量的经验数据，并将其拆分为不同的batch数组。

        参数:
            batch_size (int): 采样的经验数据数量。

        返回:
            tuple: 包含状态、动作、奖励、下一个状态、下一个动作和终止标志的numpy数组。
        """
        # batch = random.sample(self.buffer, batch_size, )
        # 从缓冲区中随机选择指定数量的经验数据,允许重复
        batch = random.choices(self.buffer, k=batch_size)
        # 初始化空列表，用于存储拆分后的经验数据
        states, actions, rewards, next_states, next_actions, terminals = [],[],[],[],[],[]
        for experience in batch:
            # 解包经验数据
            state, action, reward, next_state, next_action, terminal = experience
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            next_actions.append(next_action)
            terminals.append(terminal)
        # 将列表转换为numpy数组并返回
        return np.array(states),np.array(actions),np.array(rewards),np.array(next_states),np.array(next_actions),np.array(terminals)
        
    def sample_exps(self, batch_size):
        """
        从缓冲区中随机采样指定数量的经验数据。

        参数:
            batch_size (int): 采样的经验数据数量。

        返回:
            list: 包含采样经验数据的列表。
        """
        # 从缓冲区中随机采样指定数量的经验数据，不重复
        batch = random.sample(self.buffer, batch_size)
        return batch