import numpy as np  # 引入numpy模块，需提前安装
# import networkx as nx  # 引入numpy模块，需提前安装，用于绘制有向图
# import matplotlib.pyplot as plt  # 引入matplotlib模块，同样用于绘制有向图
# import pylab

# ---------------------------------------------------------------------
print("请输入有向图的邻接矩阵：")
n = int(input())  # 输入矩阵
a = []
print("\n你输入的矩阵为：")
for _ in range(n):
    a.append(list(map(int, input().rstrip().split())))
for i in range(n):
    print(a[i])
x = np.array(a)  # 利用numpy库将输入的列表转换为numpy中矩阵
value_1 = value_2 = sum_1 = sum_2 = sum_3 = sum_4 = y = final = x  # 分别定义value_1,sum_1,sum_2等变量(这里代码写的很恶心）
y = x + x.T
for i in range(1, n):  # 计算可达矩阵-此处可参考上图所给出的可达矩阵数学求解方法
    value_1 = np.matmul(value_1, x)
    sum_1 = sum_1 + value_1
sum_2 = sum_1 + np.identity(n)

reachability_matrix = sum_2 > 0.5  # 此处将其sum_2矩阵中所有大于0.5的矩阵元素转换为布尔值True，其余元素(均为0)转换为False

print("此有向图的可达矩阵为：")
print(reachability_matrix.astype(int))  # 得到布尔型矩阵，可将布尔类型数据(True-False)相应转化为数值型(0-1)矩阵-即可达矩阵

final = reachability_matrix + reachability_matrix.T

for i in range(1, n):
    value_2 = np.matmul(value_2, y)
    sum_3 = sum_3 + value_2
    sum_4 = sum_3 + np.identity(n)
    reachability_matrix_1 = sum_4 > 0.5
# ---------------------------------------------------------------------
# 给出判断结果
if ((reachability_matrix.astype(int) == np.ones((n, n)).astype(int)).all()):
    print("此有向线图G为强连通图或其为无向连通图")
    # print(np.ones((n,n)).astype(int))默认生成全1矩阵其中元素为float型，要多加注意
elif ((final.astype(int) == np.ones((n, n)).astype(int)).all()):
    print("此有向线图G是单向连通图")
elif ((reachability_matrix_1.astype(int) == np.ones((n, n)).astype(int)).all()):
    print("此有向线图G是弱连通图")
else:
    print("此有向图不连通")
