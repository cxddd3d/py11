# 导入 matplotlib 库中的 pyplot 模块，用于绘制图形
import matplotlib.pyplot as plt
# 导入 mpl_toolkits.mplot3d 中的 Axes3D 类，用于创建 3D 图形
from mpl_toolkits.mplot3d import Axes3D
# 导入 numpy 库，用于数值计算
import numpy as np

# 定义一个名为 draw 的函数，用于绘制状态值的 3D 图和 2D 热力图，并在热力图上标注策略
def draw(state_value, policy ):
    # 生成一个从 0 到 5 的包含 5 个元素的一维数组
    x = np.linspace(0,5,5)
    # 生成一个从 0 到 5 的包含 5 个元素的一维数组
    y = np.linspace(0,5,5)
    
    # 使用 meshgrid 函数将 x 和 y 数组转换为二维网格坐标数组
    X, Y = np.meshgrid(x,y)
    
    # 创建一个新的图形对象
    fig = plt.figure()
    # 在图形中添加一个子图，该子图占据 1 行 2 列的第 1 个位置，并且设置为 3D 投影
    ax1 = fig.add_subplot(121, projection = '3d')
    # 绘制 3D 曲面图，使用 state_value 作为 z 值，颜色映射为 'summer'
    ax1.plot_surface(Y,X,state_value, cmap='summer')
    # 设置 3D 子图的标题
    ax1.set_title('3D Plot')

    # 在图形中添加一个子图，该子图占据 1 行 2 列的第 2 个位置
    ax2 = fig.add_subplot(122)
    # 绘制 2D 热力图，使用 state_value 作为数据，颜色映射为 'summer'，原点位于左上角
    im = ax2.imshow(state_value, cmap='summer',origin='upper')
    # 设置 2D 子图的标题
    ax2.set_title('2D Heatmap')

    # 遍历 X 数组的每一行，绘制 2D 子图上的文本注释
    for i in range(len(X)):
        # 遍历 Y 数组的每一列
        for j in range(len(Y)):
            # 在 2D 热力图上每个位置添加文本注释，显示对应位置的状态值，保留两位小数
            text = ax2.text(j,i, round(state_value[i][j], 2),ha='center',va='center',color='black',alpha=1,fontsize=8)

    # 定义一个包含方向标识的列表
    logos = ['↑','→','↓','←','○']

    # 遍历 X 数组的每一行，绘制 2D 子图上的箭头
    for i in range(len(X)):
        # 遍历 Y 数组的每一列
        for j in range(len(Y)):
            # 在 2D 热力图上每个位置添加文本注释，显示对应位置的策略标识
            text = ax2.text(j,i, logos[policy[i*5+j]],ha='center',va='center',color='pink',alpha=0.6,fontsize=30)
    # 在图形中添加颜色条，用于显示热力图的颜色映射关系
    plt.colorbar(im)
    # 显示绘制好的图形
    plt.show()