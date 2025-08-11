import os  # 导入操作系统模块，用于文件路径操作
import torch  # 导入PyTorch库，用于深度学习
import torch.nn as nn  # 导入神经网络模块
import torch.nn.functional as F  # 导入函数式API
import torch.optim as optim  # 导入优化器模块
from torch.distributions import Categorical  # 导入分类分布，用于采样动作
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler  # 导入批量采样器，用于训练数据批处理
import numpy as np  # 导入NumPy库，用于数值计算


class PolicyNet(torch.nn.Module):  # 定义策略网络类，继承自PyTorch的Module,这个是演员
    def __init__(self, state_dim, hidden_dim, action_dim):  # 初始化函数，接收状态维度、隐藏层维度和动作维度
        super(PolicyNet, self).__init__()  # 调用父类初始化
        self.net1 = nn.Sequential(  # 定义网络结构为序列模型
            nn.Linear(state_dim, hidden_dim),  # 第一层线性层，输入维度为状态维度，输出维度为隐藏层维度
            nn.LeakyReLU(),  # 使用LeakyReLU激活函数
            nn.Linear(hidden_dim, hidden_dim),  # 第二层线性层，输入和输出维度都是隐藏层维度
            nn.LeakyReLU(),  # 使用LeakyReLU激活函数
            nn.Linear(hidden_dim, action_dim)  # 第三层线性层，输入维度为隐藏层维度，输出维度为动作维度
        )
    
    def forward(self, x):  # 前向传播函数
        x = self.net1(x)  # 通过网络处理输入
        return F.softmax(x, dim=1)  # 使用softmax函数将输出转换为概率分布

class ValueNet(torch.nn.Module):  # 定义价值网络类，继承自PyTorch的Module，这个是评论家
    def __init__(self, state_dim, hidden_dim):  # 初始化函数，接收状态维度和隐藏层维度
        super(ValueNet, self).__init__()  # 调用父类初始化
        self.net1 = nn.Sequential(  # 定义网络结构为序列模型
            nn.Linear(state_dim, hidden_dim),  # 第一层线性层，输入维度为状态维度，输出维度为隐藏层维度
            nn.LeakyReLU(),  # 使用LeakyReLU激活函数
            nn.Linear(hidden_dim, hidden_dim),  # 第二层线性层，输入和输出维度都是隐藏层维度
            nn.LeakyReLU(),  # 使用LeakyReLU激活函数
            nn.Linear(hidden_dim, 1)  # 第三层线性层，输入维度为隐藏层维度，输出维度为1（价值估计）
        )

    def forward(self, x):  # 前向传播函数
        x = self.net1(x)  # 通过网络处理输入
        return x  # 返回价值估计


class PPO:  # 定义PPO算法类
    def __init__(self, state_dim, hidden_dim, action_dim, device,  # 初始化函数，接收基本参数
                # the keyword arguments is only needed for pretraining / finetuning
                    num_steps=100, batch_size=4096, actor_lr=1e-4, critic_lr=1e-4, entropy_coef=1e-4, gamma=0.99, 
                    num_update_per_iter=10, clip_param=0.2, max_grad_norm=5.0):  # 接收超参数
        super(PPO, self).__init__()  # 调用父类初始化
        self.device = device  # 设置设备（CPU或GPU）
        self.state_dim = state_dim  # 设置状态维度
        self.hidden_dim = hidden_dim  # 设置隐藏层维度
        self.action_dim = action_dim  # 设置动作维度
        self.num_steps = num_steps  # 设置步数
        self.actor_net = PolicyNet(self.state_dim, self.hidden_dim, self.action_dim).to(self.device)  # 创建策略网络并移至指定设备
        self.critic_net = ValueNet(self.state_dim, self.hidden_dim).to(self.device)  # 创建价值网络并移至指定设备
        self.actor_optimizer = optim.Adam(self.actor_net.parameters(), lr=actor_lr)  # 创建策略网络优化器
        self.critic_optimizer = optim.Adam(self.critic_net.parameters(), lr=critic_lr)  # 创建价值网络优化器
        self.entropy_coef = entropy_coef  # 设置熵系数，用于鼓励探索
        self.gamma = gamma  # 设置折扣因子
        self.batch_size = batch_size  # 设置批量大小
        self.num_update_per_iter = num_update_per_iter  # 设置每次迭代的更新次数
        self.clip_param = clip_param  # 设置裁剪参数，用于限制策略更新幅度
        self.max_grad_norm = max_grad_norm  # 设置最大梯度范数，用于梯度裁剪

        self.buffer = []  # 初始化经验缓冲区
        self.buffer_size = 0  # 初始化缓冲区大小

        
        self.training_step = 0  # 初始化训练步数
        
    def select_action(self, state):  # 选择动作的函数
        if state.dtype == np.object_:  # 如果状态类型是对象
            state = np.array(state.tolist(), dtype=np.float32)  # 将其转换为浮点数数组
        # bs, obs_dim
        state = torch.from_numpy(state).float().to(self.device)  # 将状态转换为张量并移至指定设备
        with torch.no_grad():  # 不计算梯度
            # bs, act_dim
            all_action_prob = self.actor_net(state)  # 获取所有动作的概率
        c = Categorical(all_action_prob)  # 创建分类分布，用于从概率分布中采样动作
        # bs
        action = c.sample()  # 从分布中采样动作，返回一个张量，表示采样动作的索引，形状为(batch_size,)，类似topk
        # bs, act_dim
        action_onehot = F.one_hot(action, self.action_dim).float()  # 将动作转换为独热编码
        # bs
        action_prob = all_action_prob.gather(1, action.view(-1,1)).squeeze(1)  # 获取所选动作的概率
        return action_onehot.cpu().numpy(), action.cpu().numpy(), action_prob.cpu().numpy(), all_action_prob.cpu().numpy()  # 返回动作的独热编码、动作索引、动作概率和所有动作概率
    
    def save_params(self, path):  # 保存参数的函数
        save_dict = {'actor': self.actor_net.state_dict(), 'critic': self.critic_net.state_dict()}  # 创建包含策略网络和价值网络参数的字典
        name = path+'.pt'  # 设置保存文件名
        torch.save(save_dict, name, _use_new_zipfile_serialization=False)  # 保存参数到文件

    def load_params(self, filename):  # 加载参数的函数
        save_dict = torch.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), map_location=self.device)  # 从文件加载参数
        self.actor_net.load_state_dict(save_dict['actor'])  # 加载策略网络参数
        self.critic_net.load_state_dict(save_dict['critic'])  # 加载价值网络参数
    
    def load_params_from_policy(self, policy):  # 从另一个策略加载参数的函数
        self.actor_net.load_state_dict(policy.actor_net.state_dict())  # 加载策略网络参数
        self.critic_net.load_state_dict(policy.critic_net.state_dict())  # 加载价值网络参数

    def store_transition(self, transition):  # 存储转换的函数
        self.buffer.append(transition)  # 将转换添加到缓冲区
        self.buffer_size += 1  # 增加缓冲区大小
        
    def update(self):  # 更新网络的函数
        state, action, a_prob, G = [], [], [], []  # 初始化状态、动作、动作概率和回报列表
        state = torch.tensor([t.state for t in self.buffer], dtype=torch.float32)  # 从缓冲区提取状态并转换为张量
        action = torch.tensor([[t.action] for t in self.buffer], dtype=torch.int64)  # 从缓冲区提取动作并转换为张量
        old_action_prob = torch.tensor([t.a_prob for t in self.buffer], dtype=torch.float32)  # 从缓冲区提取动作概率并转换为张量
        G = torch.tensor([t.G for t in self.buffer], dtype=torch.float32)  # 从缓冲区提取回报并转换为张量
        
        # non_zero_indices = G != 0  # 获取非零回报的索引
        # state = state[non_zero_indices]  # 筛选非零回报对应的状态
        # action = action[non_zero_indices]  # 筛选非零回报对应的动作
        # old_action_prob = old_action_prob[non_zero_indices]  # 筛选非零回报对应的动作概率
        # G = G[non_zero_indices]  # 筛选非零回报
        
        actor_loss, critic_loss, entropy, loss_count = 0., 0., 0., 0.  # 初始化损失和计数器
        for _ in range(self.num_update_per_iter):  # 对每次迭代进行多次更新
            for index in BatchSampler(SubsetRandomSampler(range(len(state))), self.batch_size, False):  # 对数据进行批量采样
                s_batch = state[index]  # 获取状态批次
                a_batch = action[index]  # 获取动作批次
                old_action_prob_batch = old_action_prob[index]  # 获取旧动作概率批次
                G_batch = G[index].view(-1,1)  # 获取回报批次并调整形状
                V_batch = self.critic_net(s_batch)  # 使用价值网络估计价值
                delta = G_batch - V_batch  # 计算优势函数
                advantage = delta.detach().clone()  # 分离优势函数，防止梯度传播

                all_action_prob_batch = self.actor_net(s_batch)  # 使用策略网络获取所有动作概率
                entropy_ = Categorical(all_action_prob_batch).entropy().mean()  # 计算策略的熵
                action_prob_batch = all_action_prob_batch.gather(1, a_batch)  # 获取所选动作的概率（新策略）
                ratio = (action_prob_batch / old_action_prob_batch)  # 计算新旧策略的比率
            
                surr1 = ratio * advantage  # 计算第一个替代目标
                surr2 = torch.clamp(ratio, 1-self.clip_param, 1+self.clip_param) * advantage  # 计算第二个替代目标（带裁剪）
                action_loss = -torch.min(surr1, surr2).mean()  # 取两个目标的最小值，并取负（转为最大化问题）
                act_loss = action_loss - self.entropy_coef * entropy_  # 加入熵正则化项
                
                self.actor_optimizer.zero_grad()  # 清空策略网络梯度
                act_loss.backward()  # 反向传播计算梯度
                nn.utils.clip_grad_norm_(self.actor_net.parameters(), self.max_grad_norm)  # 裁剪梯度
                self.actor_optimizer.step()  # 更新策略网络参数
                value_loss = F.mse_loss(V_batch, G_batch)  # 计算价值网络的均方误差损失
                self.critic_optimizer.zero_grad()  # 清空价值网络梯度
                value_loss.backward()  # 反向传播计算梯度
                nn.utils.clip_grad_norm_(self.critic_net.parameters(), self.max_grad_norm)  # 裁剪梯度
                self.critic_optimizer.step()  # 更新价值网络参数

                self.training_step += 1  # 增加训练步数
                actor_loss += action_loss.item()  # 累加策略损失
                critic_loss += value_loss.item()  # 累加价值损失
                entropy += entropy_.item()  # 累加熵
                
                loss_count += 1  # 增加损失计数
        # print(loss_count)  # 打印损失计数
        # clear experience
        self.buffer = []  # 清空经验缓冲区
        self.buffer_size = 0  # 重置缓冲区大小
        
        torch.cuda.empty_cache()  # 清空CUDA缓存
        
        return actor_loss/loss_count, critic_loss/loss_count, entropy/loss_count  # 返回平均损失和熵
