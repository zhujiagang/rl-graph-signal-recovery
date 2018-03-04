#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2017/7/20 10:48
# @Author : Lyrichu
# @Email  : 919987476@qq.com
# @File   : improve_random_walk.py
'''
@Description:改进的随机游走算法
这里求解:f = sin(r)/r + 1,r = sqrt((x-50)^2+(y-50)^2)+e,0<=x,y<=100 的最大值
求解f的最大值，可以转化为求-f的最小值问题
'''
from __future__  import print_function
import math
import random
N = 100 # 迭代次数
step = 10.0 # 初始步长
epsilon = 0.00001
variables = 2 # 变量数目
x = [-100,-10] # 初始点坐标
walk_num = 1 # 初始化随机游走次数
n = 10 # 每次随机生成向量u的数目
print("迭代次数:",N)
print("初始步长:",step)
print("每次产生随机向量数目:",n)
print("epsilon:",epsilon)
print("变量数目:",variables)
print("初始点坐标:",x)
# 定义目标函数
def function(x):
    r = math.sqrt((x[0]-50)**2 + (x[1]-50)**2) + math.e
    f = math.sin(r)/r + 1
    return -f
# 开始随机游走
while(step > epsilon):
    k = 1 # 初始化计数器
    while(k < N):
        # 产生n个向量u
        x1_list = [] # 存放x1的列表
        for i in range(n):
            u = [random.uniform(-1,1) for i1 in range(variables)] # 随机向量
            # u1 为标准化之后的随机向量
            u1 = [u[i3]/math.sqrt(sum([u[i2]**2 for i2 in range(variables)])) for i3 in range(variables)]
            x1 = [x[i4] + step*u1[i4] for i4 in range(variables)]
            x1_list.append(x1)
        f1_list = [function(x1) for x1 in x1_list]
        f1_min = min(f1_list)
        f1_index = f1_list.index(f1_min)
        x11 = x1_list[f1_index] # 最小f1对应的x1
        if(f1_min < function(x)): # 如果找到了更优点
            k = 1
            x = x11
        else:
            k += 1
    step = step/2
    print("第%d次随机游走完成。" % walk_num)
    walk_num += 1
print("随机游走次数:",walk_num-1)
print("最终最优点:",x)
print("最终最优值:",function(x))