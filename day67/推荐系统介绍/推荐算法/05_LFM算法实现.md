## 基于矩阵分解的CF算法实现（一）：LFM

LFM也就是前面提到的Funk SVD矩阵分解

#### LFM原理解析(latent factor model)

LFM隐语义模型核心思想是通过隐含特征联系用户和物品，如下图：

![](./img/LFM矩阵分解图解.png)

- P矩阵是User-LF矩阵，即用户和隐含特征矩阵。LF有三个，表示共总有三个隐含特征。
- Q矩阵是LF-Item矩阵，即隐含特征和物品的矩阵
- R矩阵是User-Item矩阵，有P*Q得来
- **能处理稀疏评分矩阵**

利用矩阵分解技术，将原始User-Item的评分矩阵（稠密/稀疏）分解为P和Q矩阵，然后利用$P*Q$还原出User-Item评分矩阵$R$。整个过程相当于降维处理，其中：

- 矩阵值$P_{11}$表示用户1对隐含特征1的权重值

- 矩阵值$Q_{11}$表示隐含特征1在物品1上的权重值

- 矩阵值$R_{11}$就表示预测的用户1对物品1的评分，且$R_{11}=\vec{P_{1,k}}\cdot \vec{Q_{k,1}}$

  ![](./img/LFM矩阵分解图解2.png)

利用LFM预测用户对物品的评分，$k$表示隐含特征数量：
$$
\begin{split}
\hat {r}_{ui} &=\vec {p_{uk}}\cdot \vec {q_{ik}}
\\&={\sum_{k=1}}^k p_{uk}q_{ik}
\end{split}
$$
因此最终，我们的目标也就是要求出P矩阵和Q矩阵及其当中的每一个值，然后再对用户-物品的评分进行预测。

#### 损失函数

同样对于评分预测我们利用平方差来构建损失函数：
$$
\begin{split}
Cost &= \sum_{u,i\in R} (r_{ui}-\hat{r}_{ui})^2
\\&=\sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})^2
\end{split}
$$
加入L2正则化：
$$
Cost = \sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})^2 + \lambda(\sum_U{p_{uk}}^2+\sum_I{q_{ik}}^2)
$$
对损失函数求偏导：
$$
\begin{split}
\cfrac {\partial}{\partial p_{uk}}Cost &= \cfrac {\partial}{\partial p_{uk}}[\sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})^2 + \lambda(\sum_U{p_{uk}}^2+\sum_I{q_{ik}}^2)]
\\&=2\sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})(-q_{ik}) + 2\lambda p_{uk}
\\\\
\cfrac {\partial}{\partial q_{ik}}Cost &= \cfrac {\partial}{\partial q_{ik}}[\sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})^2 + \lambda(\sum_U{p_{uk}}^2+\sum_I{q_{ik}}^2)]
\\&=2\sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})(-p_{uk}) + 2\lambda q_{ik}
\end{split}
$$

#### 随机梯度下降法优化

偏导的基础上乘以学习率，梯度下降更新参数$p_{uk}$：
$$
\begin{split}
p_{uk}&:=p_{uk} - \alpha\cfrac {\partial}{\partial p_{uk}}Cost
\\&:=p_{uk}-\alpha [2\sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})(-q_{ik}) + 2\lambda p_{uk}]
\\&:=p_{uk}+\alpha [\sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})q_{ik} - \lambda p_{uk}]
\end{split}
$$
 同理：
$$
\begin{split}
q_{ik}&:=q_{ik} + \alpha[\sum_{u,i\in R} (r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})p_{uk} - \lambda q_{ik}]
\end{split}
$$
**随机梯度下降：** 向量乘法 每一个分量相乘 求和
$$
\begin{split}
&p_{uk}:=p_{uk}+\alpha [(r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})q_{ik} - \lambda_1 p_{uk}]
\\&q_{ik}:=q_{ik} + \alpha[(r_{ui}-{\sum_{k=1}}^k p_{uk}q_{ik})p_{uk} - \lambda_2 q_{ik}]
\end{split}
$$
由于P矩阵和Q矩阵是两个不同的矩阵，通常分别采取不同的正则参数，如$\lambda_1$和$\lambda_2$，随机梯度下降是$p_{uk}$和$q_{ik}$初始是随机的

**算法实现**

```python
'''
LFM Model
'''
import pandas as pd
import numpy as np

# 评分预测    1-5
class LFM(object):

    def __init__(self, alpha, reg_p, reg_q, number_LatentFactors=10, number_epochs=10, columns=["uid", "iid", "rating"]):
        self.alpha = alpha # 学习率
        self.reg_p = reg_p    # P矩阵正则
        self.reg_q = reg_q    # Q矩阵正则
        self.number_LatentFactors = number_LatentFactors  # 隐式类别数量
        self.number_epochs = number_epochs    # 最大迭代次数
        self.columns = columns

    def fit(self, dataset):
        '''
        fit dataset
        :param dataset: uid, iid, rating
        :return:
        '''

        self.dataset = pd.DataFrame(dataset)

        self.users_ratings = dataset.groupby(self.columns[0]).agg([list])[[self.columns[1], self.columns[2]]]
        self.items_ratings = dataset.groupby(self.columns[1]).agg([list])[[self.columns[0], self.columns[2]]]

        self.globalMean = self.dataset[self.columns[2]].mean()

        self.P, self.Q = self.sgd()

    def _init_matrix(self):
        '''
        初始化P和Q矩阵，同时为设置0，1之间的随机值作为初始值
        :return:
        '''
        # User-LF
        P = dict(zip(
            self.users_ratings.index,
            np.random.rand(len(self.users_ratings), self.number_LatentFactors).astype(np.float32)
        ))
        # Item-LF
        Q = dict(zip(
            self.items_ratings.index,
            np.random.rand(len(self.items_ratings), self.number_LatentFactors).astype(np.float32)
        ))
        return P, Q

    def sgd(self):
        '''
        使用随机梯度下降，优化结果
        :return:
        '''
        P, Q = self._init_matrix()

        for i in range(self.number_epochs):
            print("iter%d"%i)
            error_list = []
            for uid, iid, r_ui in self.dataset.itertuples(index=False):
                # User-LF P
                ## Item-LF Q
                v_pu = P[uid] #用户向量
                v_qi = Q[iid] #物品向量
                #np.dot(v_pu, v_qi)是两个矩阵相乘
                err = np.float32(r_ui - np.dot(v_pu, v_qi))
				#这里和上面的公式是完全对应的
                v_pu += self.alpha * (err * v_qi - self.reg_p * v_pu)
                v_qi += self.alpha * (err * v_pu - self.reg_q * v_qi)
                
                P[uid] = v_pu 
                Q[iid] = v_qi
				#注释是另外一种方式
                # for k in range(self.number_of_LatentFactors):
                #     v_pu[k] += self.alpha*(err*v_qi[k] - self.reg_p*v_pu[k])
                #     v_qi[k] += self.alpha*(err*v_pu[k] - self.reg_q*v_qi[k])
				#把误差记录在列表中
                error_list.append(err ** 2)
            #打印误差的平均值
            print(np.sqrt(np.mean(error_list)))
        return P, Q

    def predict(self, uid, iid):
        # 如果uid或iid不在，我们使用全剧平均分作为预测结果返回
        if uid not in self.users_ratings.index or iid not in self.items_ratings.index:
            return self.globalMean

        p_u = self.P[uid]
        q_i = self.Q[iid]

        return np.dot(p_u, q_i)

    def test(self,testset):
        '''预测测试集数据'''
        for uid, iid, real_rating in testset.itertuples(index=False):
            try:
                pred_rating = self.predict(uid, iid)
            except Exception as e:
                print(e)
            else:
                yield uid, iid, real_rating, pred_rating

if __name__ == '__main__':
    dtype = [("userId", np.int32), ("movieId", np.int32), ("rating", np.float32)]
    dataset = pd.read_csv("datasets/ml-latest-small/ratings.csv", usecols=range(3), dtype=dict(dtype))

    lfm = LFM(0.02, 0.01, 0.01, 10, 100, ["userId", "movieId", "rating"])
    lfm.fit(dataset)

    while True:
        uid = input("uid: ")
        iid = input("iid: ")
        print(lfm.predict(int(uid), int(iid)))

```



总结：

在了解了矩阵分解的原理之后，就可以更清楚地解释为什么矩阵分解相较协同过滤有更强的泛化能力。在矩阵分解算法中，由于隐向量的存在，**使任意的用户和物品之间都可以得到预测分值**。而隐向量的生成过程其实是对共现矩阵进行全局拟合的过程，因此隐向量其实是利用全局信息生成的，有更强的泛化能力;**而对协同过滤来说，如果两个用户没有相同的历史行为，两个物品没有相同的人购买，那么这两个用户和两个物品的相似度都将为0**(因为协同过滤只能利用用户和物品自己的信息进行相似度计算，这就使协同过滤不具备泛化利用全局信息的能力) 。



(1）泛化能力强。在一定程度上解决了数据稀疏问题。
(2）空间复杂度低。不需再存储协同过滤模型服务阶段所需的“庞大”的用户相似性或物品相似性矩阵，只需存储用户和物品隐向量。空间复杂度由$n^2$级别降低到(n+m)·k级别。
(3）**更好的扩展性和灵活性。矩阵分解的最终产出是用户和物品隐向量，这其实与深度学习中的Embedding思想不谋而合，**因此矩阵分解的结果也非常便于与其他特征进行组合和拼接，并便于与深度学习网络进行无缝结合。
与此同时，也要意识到矩阵分解的局限性。与协同过滤一样，**矩阵分解同样不方便加入用户、物品和上下文相关的特征**，这使得矩阵分解丧失了利用很多有效信息的机会，同时在缺乏用户历史行为时，无法进行有效的推荐。为了解决这个问题，逻辑回归模型及其后续发展出的因子分解机等模型，凭借其天然的融合不同特征的能力，逐渐在推荐系统领域得到更广泛的应用。

