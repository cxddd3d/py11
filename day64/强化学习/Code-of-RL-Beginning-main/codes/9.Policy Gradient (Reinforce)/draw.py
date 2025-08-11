import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
import numpy as np

def draw(state_value, policy):
    """
    绘制状态值的3D曲面图和2D热力图，并在热力图上标注策略信息。

    :param state_value: 状态值数组，用于绘制3D曲面图和2D热力图
    :param policy: 策略数组，用于在热力图上标注策略信息
    """
    # 生成从0到5，共5个点的一维数组
    x = np.linspace(0,5,5)
    y = np.linspace(0,5,5)
    
    # 生成二维网格坐标
    X, Y = np.meshgrid(x,y)
    
    # 创建一个新的图形窗口
    fig = plt.figure()
    # 添加一个3D子图，位于1行2列的第一个位置
    ax1 = fig.add_subplot(121, projection = '3d')
    # 绘制3D曲面图
    ax1.plot_surface(Y,X,state_value, cmap='summer')
    # 设置3D子图的标题
    ax1.set_title('3D Plot')

    # 添加一个2D子图，位于1行2列的第二个位置
    ax2 = fig.add_subplot(122)
    # 绘制2D热力图
    im = ax2.imshow(state_value, cmap='summer',origin='upper')
    # 设置2D子图的标题
    ax2.set_title('2D Heatmap')

    # 在2D热力图上标注状态值
    for i in range(len(X)):
        for j in range(len(Y)):
            text = ax2.text(j,i, round(state_value[i][j], 2),ha='center',va='center',color='black',alpha=1,fontsize=8)

    # 定义策略标识符号
    logos = ['↑','→','↓','←','○']

    # 在2D热力图上标注策略信息
    for i in range(len(X)):
        for j in range(len(Y)):
            text = ax2.text(j,i, logos[policy[i*5+j]],ha='center',va='center',color='pink',alpha=0.6,fontsize=30)
    # 添加颜色条
    plt.colorbar(im)
    # 显示图形
    plt.show()

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# 示例概率数据，假设4x4的Gridworld
# now_frame_probabilities = np.random.rand(4, 4, 4)  # 随机生成每个方向的概率


def plot_policy(pre_frame_probabilities,now_frame_probabilities,trajectory_state_action_score, states_trajectory, 
                mpdesc, img_path):
    """
    pre_frame_probabilities: 上一帧的概率，是一个state_num*action_num的列表，表示当前(state,action)的几率，每一行概率和为1
    now_frame_probabilities：当前帧的概率，是一个state_num*action_num，表示当前(state,action)的几率，每一行概率和为1
    trajectory_state_action_score：这个是轨迹的得分，这是一个state_num*action_num二维的list，第一维是state(0~state_num)，第二维是对应的动作，数组的元素是当前state执行这个动作的奖励（至于是累计奖励还是平均奖励，都可以），便于打印
    states_trajectory：是一个元组列表，注意这里不一样了，这里的元素是（x,y）元组，表示当前state的x,y坐标，然后依次进行轨迹打印
    mpdesc是地图属性，应该为env.get_map_description()传递进来
    img_path是当前这个图片保存的图片位置
    
    
    下面这段是测试代码
        now_frame_probabilities = np.random.rand(25, 4)  # 随机生成每个方向的概率
        pre_frame_probabilities = np.random.rand(25, 4)  # 随机生成每个方向的概率
        trajectory_state_action_score = np.zeros((25,4))  # 初始化每个方向的得分
        
        mpdesc = [".....",".##..","..#..",".#T#.",".#..."]
        states = [[1,2],[1,3]]
        trajectory_state_action_score[7][1] = -9.7
        trajectory_state_action_score[8][2] = 30
        
        trajectory_state_action_score[9][2] = -9.9
        
        # img_path 
        plot_policy(pre_frame_probabilities, now_frame_probabilities,trajectory_state_action_score, states, mpdesc, img_path=None)
    """
    mp = mpdesc
    
    # 获取地图的行数
    rows = len(mp)
    # 获取地图的列数
    columns = len(mp[0])
    
    # states_trajectory.append([3,2]) # 把最后目的地加入进去，方面画图
    
    # 创建一个包含3个子图的图形窗口
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(11, 4))

    # 获取上一帧概率子图
    ax_pre_frame_probabilities = axs[0]
    # 获取轨迹子图
    ax_trajectory = axs[1]
    # 获取当前帧概率子图
    ax_now_frame_probabilities = axs[2]

    # 设置上一帧概率子图的标题
    ax_pre_frame_probabilities.set_title('pre frame', fontproperties='SimHei', fontsize=10)
    # 设置轨迹子图的标题
    ax_trajectory.set_title('trajectory', fontproperties='SimHei', fontsize=10)
    # 设置当前帧概率子图的标题
    ax_now_frame_probabilities.set_title('now frame', fontproperties='SimHei', fontsize=10)

    #########################################################################################################################
    ##############################################      上一帧的概率可视化      ###############################################
    #########################################################################################################################

    # 箭头宽度
    arrow_width = 1
    # 动作列表
    actions = None
    # 动作方向字典
    directions = None
    # 偏移量
    offset = None
    # 箭头偏移量
    offset_arraw = None  
    # 文本偏移量
    offset_text = None  
    
    # 根据动作数量初始化动作列表、偏移量和方向字典
    if len(pre_frame_probabilities[0])==5:
        actions = ['up', 'right', 'down', 'left', 'stay']
        offset_arraw = 0.1
        offset_text = 0.1
        directions = {'up': (0, 0.7), 'right': (0.7, 0), 'down': (0, -0.7), 'left': (-0.7, 0), 'stay': (0, 0)}
    else:
        actions = ['up', 'right', 'down', 'left']
        offset_arraw = 0.04
        offset_text = 0.06
        offset = 0.0
        
        directions = {'up': (0, 0.8), 'right': (0.8, 0), 'down': (0, -0.8), 'left': (-0.8, 0), 'stay': (0, 0)}
    # 绘制地图网格
    mp = mpdesc
    for i in range(rows):
        for j in range(columns):
            if mp[i][j] == '.':
                color = 'white'
            if mp[i][j] == '#':
                color = '#F5C142'
            if mp[i][j] == 'T':
                color = '#65FFFF'  
            # 添加矩形表示地图格子
            ax_pre_frame_probabilities.add_patch(plt.Rectangle((j, rows -1 - i), 1, 1, facecolor=color, edgecolor='black', linewidth=0.2))
            
    # 绘制水平和垂直线条
    for x in range(6):
        ax_pre_frame_probabilities.axhline(x, lw=0.2, color='black', zorder=0)
        ax_pre_frame_probabilities.axvline(x, lw=0.2, color='black', zorder=0)
        
    
    # 定义箭头偏移量字典
    offsets_arraw = {
    'up': (0, offset_arraw),
    'right': (offset_arraw, 0),
    'down': (0, -offset_arraw),
    'left': (-offset_arraw, 0),
    'stay': (0, 0)
    }
    # 定义文本偏移量字典
    offsets_text = {
    'up': (0, offset_text),
    'right': (offset_text, 0),
    'down': (0, -offset_text),
    'left': (-offset_text, 0),
    'stay': (0, 0)
    }
    # 绘制箭头
    for i in range(rows):
        for j in range(columns):
            for k, action in enumerate(actions):
                # 获取动作方向
                dx, dy = directions[action]
                
                # 获取动作概率
                prob = pre_frame_probabilities[i*columns+j][k]
                
                # 获取箭头和文本偏移量
                ox_a, oy_a = offsets_arraw[action]
                ox_t, oy_t = offsets_text[action]

                # 初始化箭头颜色、样式和长度比例
                color = "gray"
                arrowstyle = "-"
                len_scale = 0.3
                # 如果是最大概率动作，修改颜色、样式和长度比例
                if k == np.array(pre_frame_probabilities[i*columns+j]).argmax():
                    color = "red"
                    arrowstyle = '->'
                    len_scale = 0.37
                
                if action == 'stay':
                    # 用圆圈表示不动的动作
                    circle = plt.Circle((j + 0.5 , rows-0.5  - i ), 0.1, color=color, fill=False, linewidth=1)
                    ax_pre_frame_probabilities.add_patch(circle)
                    ax_pre_frame_probabilities.text(j + 0.5 + ox, rows-0.5  - i + oy, f'{prob*100:.0f}', color=color, ha='center', va='center', fontsize=7)
                
                # 创建箭头并添加到子图
                arrow = FancyArrowPatch((j + 0.5+ ox_a, rows-1 - i + 0.5+ oy_a), (j + 0.5 + dx * len_scale, rows-1 - i + 0.5 + dy * len_scale),
                                        arrowstyle=arrowstyle, mutation_scale=5, lw=arrow_width, color=color)
                ax_pre_frame_probabilities.add_patch(arrow)
                # 添加概率文本
                ax_pre_frame_probabilities.text(j + 0.5 + ox_a + dx * 0.3+ox_t, rows-0.5  - i + oy_a + dy * 0.3+oy_t, f'{prob*100:.0f}', color=color, ha='center', va='center', fontsize=7)
                
    # 设置子图的坐标轴范围
    ax_pre_frame_probabilities.set_xlim(-0.05, columns + 0.05)
    ax_pre_frame_probabilities.set_ylim(-0.05, rows + 0.05)
    # 设置子图的纵横比为1:1
    ax_pre_frame_probabilities.set_aspect('equal')
    # 隐藏坐标轴
    ax_pre_frame_probabilities.axis('off')



    #########################################################################################################################
    ##########################################           轨迹绘制             ################################################
    #########################################################################################################################
    
    # 箭头宽度
    arrow_width = 1
    # 动作列表
    actions = ['up', 'right', 'down', 'left', 'stay']
    # 动作方向字典
    directions = {'up': (0, 0.7), 'right': (0.7, 0), 'down': (0, -0.7), 'left': (-0.7, 0), 'stay': (0, 0)}
    # 绘制地图网格
    for i in range(rows):
        for j in range(columns):
            if mp[i][j] == '.':
                color = 'white'
            if mp[i][j] == '#':
                color = '#F5C142'
            if mp[i][j] == 'T':
                color = '#65FFFF'  
            # 添加矩形表示地图格子
            ax_trajectory.add_patch(plt.Rectangle((j, rows-1 - i), 1, 1, facecolor=color, edgecolor='black', linewidth=0.2))
            
    # 绘制水平和垂直线条
    for x in range(6):
        ax_trajectory.axhline(x, lw=0.2, color='black', zorder=0)
        ax_trajectory.axvline(x, lw=0.2, color='black', zorder=0)

    # 绘制前250个轨迹点或全部轨迹点（取较小值）
    left = min(len(states_trajectory) - 1,250)
    for i in range(left):
        # 获取起点坐标
        start = states_trajectory[i]
        start = (start[1],rows-1-start[0])
        # 获取终点坐标
        end = states_trajectory[i + 1]
        end = (end[1],rows-1-end[0])
        # 计算带有随机偏移的箭头方向
        dx = end[0] - start[0] + np.random.uniform(-0.15, 0.15)  # 添加随机偏移
        dy = end[1] - start[1] + np.random.uniform(-0.15, 0.15)  # 添加随机偏移
        # 透明度
        alpha = 0.2
        # 颜色强度
        color_intensity = np.clip(alpha, 0, 1)
        # color = (color_intensity, 0, 1 - color_intensity)  # 颜色从浅蓝变为深蓝
        color = "black"
        # 绘制箭头
        ax_trajectory.arrow(start[0]+0.5, start[1]+0.5, dx, dy, head_width=0.1, head_length=0.1, fc=color, ec=color, alpha=0.2)
    
    # 绘制剩余的轨迹点
    for i in range(max(len(states_trajectory)-250, left), len(states_trajectory)-1):
        # 获取起点坐标
        start = states_trajectory[i]
        start = (start[1],rows-1-start[0])
        # 获取终点坐标
        end = states_trajectory[i + 1]
        end = (end[1],rows-1-end[0])
        # 计算带有随机偏移的箭头方向
        dx = end[0] - start[0] + np.random.uniform(-0.15, 0.15)  # 添加随机偏移
        dy = end[1] - start[1] + np.random.uniform(-0.15, 0.15)  # 添加随机偏移
        # 透明度
        alpha = 0.2
        # 颜色强度
        color_intensity = np.clip(alpha, 0, 1)
        # color = (color_intensity, 0, 1 - color_intensity)  # 颜色从浅蓝变为深蓝
        color = "black"
        # 绘制箭头
        ax_trajectory.arrow(start[0]+0.5, start[1]+0.5, dx, dy, head_width=0.1, head_length=0.1, fc=color, ec=color, alpha=0.2)




    # 箭头宽度
    arrow_width = 1
    # 动作列表
    actions = None
    # 动作方向字典
    directions = None
    # 偏移量
    offset = None
    # 箭头偏移量
    offset_arraw = None  
    # 文本偏移量
    offset_text = None  
    
    # 根据动作数量初始化动作列表、偏移量和方向字典
    if len(now_frame_probabilities[0])==5:
        actions = ['up', 'right', 'down', 'left', 'stay']
        offset_arraw = 0.1
        offset_text = 0.1
        directions = {'up': (0, 0.7), 'right': (0.7, 0), 'down': (0, -0.7), 'left': (-0.7, 0), 'stay': (0, 0)}
    else:
        actions = ['up', 'right', 'down', 'left']
        offset_arraw = 0.04
        offset_text = 0.06
        offset = 0.0
        
        directions = {'up': (0, 0.8), 'right': (0.8, 0), 'down': (0, -0.8), 'left': (-0.8, 0), 'stay': (0, 0)}

    
    # 定义箭头偏移量字典
    offsets_arraw = {
    'up': (0, offset_arraw),
    'right': (offset_arraw, 0),
    'down': (0, -offset_arraw),
    'left': (-offset_arraw, 0),
    'stay': (0, 0)
    }
    # 定义文本偏移量字典
    offsets_text = {
    'up': (0, offset_text),
    'right': (offset_text, 0),
    'down': (0, -offset_text),
    'left': (-offset_text, 0),
    'stay': (0, 0)
    }
    # 绘制箭头
    for i in range(rows):
        for j in range(columns):
            for k, action in enumerate(actions):
                # 获取动作方向
                dx, dy = directions[action]
                
                # 获取动作得分
                score = trajectory_state_action_score[i*columns+j][k]
                
                # 获取箭头和文本偏移量
                ox_a, oy_a = offsets_arraw[action]
                ox_t, oy_t = offsets_text[action]

                # 初始化箭头颜色、样式和长度比例
                color = "gray"
                arrowstyle = "-"
                len_scale = 0.3
                
                # 如果得分是0，跳过该动作
                if score == 0:
                    continue

                # 初始化文本字符串
                text_str = ""
                # 限制得分范围
                score = max(-99,score)
                score = min( 99,score)
                
                
                if score > 0:
                    color = "red"
                    arrowstyle = '->'
                    len_scale = 0.37
                    if score>10:
                        text_str = f'{score:.0f}'
                    else:
                        text_str = f'{score:.1f}'
                    
                if score < 0:
                    score = -score
                    color = "blue"
                    arrowstyle = '->'
                    len_scale = 0.37
                    if score>10:
                        text_str = f'{score:.0f}'
                    else:
                        text_str = f'{score:.1f}'
                
                if action == 'stay':
                    # 用圆圈表示不动的动作
                    circle = plt.Circle((j + 0.5 , rows-0.5  - i ), 0.1, color=color, fill=False, linewidth=1)
                    # ax_trajectory.add_patch(circle)
                    ax_trajectory.text(j + 0.5 + ox, rows-0.5  - i + oy, text_str, color=color, ha='center', va='center', fontsize=6, alpha=1)
                
                # 创建箭头并添加到子图
                arrow = FancyArrowPatch((j + 0.5+ ox_a, rows-1 - i + 0.5+ oy_a), (j + 0.5 + dx * len_scale, rows-1 - i + 0.5 + dy * len_scale),
                                        arrowstyle=arrowstyle, mutation_scale=5, lw=arrow_width, color=color, alpha=0.7)
                ax_trajectory.add_patch(arrow)
                # 添加得分文本
                ax_trajectory.text(j + 0.5 + ox_a + dx * 0.3+ox_t, rows-0.5  - i + oy_a + dy * 0.3+oy_t, text_str, color=color, ha='center', va='center', fontsize=6, alpha=1)
                
    # 设置子图的坐标轴范围
    ax_trajectory.set_xlim(-0.05, columns + 0.05)
    ax_trajectory.set_ylim(-0.05, rows + 0.05)
    # 设置子图的纵横比为1:1
    ax_trajectory.set_aspect('equal')
    # 隐藏坐标轴
    ax_trajectory.axis('off')

    



    #########################################################################################################################
    ##############################################      当前帧的概率可视化      ###############################################
    #########################################################################################################################

    # 箭头宽度
    arrow_width = 1
    # 动作列表
    actions = None
    # 动作方向字典
    directions = None
    # 偏移量
    offset = None
    # 箭头偏移量
    offset_arraw = None  
    # 文本偏移量
    offset_text = None  
    
    # 根据动作数量初始化动作列表、偏移量和方向字典
    if len(now_frame_probabilities[0])==5:
        actions = ['up', 'right', 'down', 'left', 'stay']
        offset_arraw = 0.1
        offset_text = 0.1
        directions = {'up': (0, 0.7), 'right': (0.7, 0), 'down': (0, -0.7), 'left': (-0.7, 0), 'stay': (0, 0)}
    else:
        actions = ['up', 'right', 'down', 'left']
        offset_arraw = 0.04
        offset_text = 0.06
        offset = 0.0
        
        directions = {'up': (0, 0.8), 'right': (0.8, 0), 'down': (0, -0.8), 'left': (-0.8, 0), 'stay': (0, 0)}
    # 绘制地图网格
    mp = mpdesc
    for i in range(rows):
        for j in range(columns):
            if mp[i][j] == '.':
                color = 'white'
            if mp[i][j] == '#':
                color = '#F5C142'
            if mp[i][j] == 'T':
                color = '#65FFFF'  
            # 添加矩形表示地图格子
            ax_now_frame_probabilities.add_patch(plt.Rectangle((j, rows -1 - i), 1, 1, facecolor=color, edgecolor='black', linewidth=0.2))
            
    # 绘制水平和垂直线条
    for x in range(6):
        ax_now_frame_probabilities.axhline(x, lw=0.2, color='black', zorder=0)
        ax_now_frame_probabilities.axvline(x, lw=0.2, color='black', zorder=0)
        
    
    # 定义箭头偏移量字典
    offsets_arraw = {
    'up': (0, offset_arraw),
    'right': (offset_arraw, 0),
    'down': (0, -offset_arraw),
    'left': (-offset_arraw, 0),
    'stay': (0, 0)
    }
    # 定义文本偏移量字典
    offsets_text = {
    'up': (0, offset_text),
    'right': (offset_text, 0),
    'down': (0, -offset_text),
    'left': (-offset_text, 0),
    'stay': (0, 0)
    }
    # 绘制箭头
    for i in range(rows):
        for j in range(columns):
            for k, action in enumerate(actions):
                # 获取动作方向
                dx, dy = directions[action]
                
                # 获取动作概率
                prob = now_frame_probabilities[i*columns+j][k]
                
                # 获取箭头和文本偏移量
                ox_a, oy_a = offsets_arraw[action]
                ox_t, oy_t = offsets_text[action]

                # 初始化箭头颜色、样式和长度比例
                color = "gray"
                arrowstyle = "-"
                len_scale = 0.3
                # 如果是最大概率动作，修改颜色、样式和长度比例
                if k == np.array(now_frame_probabilities[i*columns+j]).argmax():
                    color = "red"
                    arrowstyle = '->'
                    len_scale = 0.37
                
                if action == 'stay':
                    # 用圆圈表示不动的动作
                    circle = plt.Circle((j + 0.5 , rows-0.5  - i ), 0.1, color=color, fill=False, linewidth=1)
                    ax_now_frame_probabilities.add_patch(circle)
                    ax_now_frame_probabilities.text(j + 0.5 + ox, rows-0.5  - i + oy, f'{prob*100:.0f}', color=color, ha='center', va='center', fontsize=7)
                
                # 创建箭头并添加到子图
                arrow = FancyArrowPatch((j + 0.5+ ox_a, rows-0.5 - i + oy_a), (j + 0.5 + dx * len_scale, rows-0.5  - i  + dy * len_scale),
                                        arrowstyle=arrowstyle, mutation_scale=5, lw=arrow_width, color=color)
                ax_now_frame_probabilities.add_patch(arrow)
                # 添加概率文本
                ax_now_frame_probabilities.text(j + 0.5 + ox_a + dx * 0.3+ox_t, rows-0.5  - i + oy_a + dy * 0.3+oy_t, f'{prob*100:.0f}', color=color, ha='center', va='center', fontsize=7)
                
    # 设置子图的坐标轴范围
    ax_now_frame_probabilities.set_xlim(-0.05, columns + 0.05)
    ax_now_frame_probabilities.set_ylim(-0.05, rows + 0.05)
    # 设置子图的纵横比为1:1
    ax_now_frame_probabilities.set_aspect('equal')
    # 隐藏坐标轴
    ax_now_frame_probabilities.axis('off')

    # 如果指定了图片保存路径，保存图片
    if img_path!=None:
        plt.savefig(img_path)
    # 显示图形
    plt.show()
