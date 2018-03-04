#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2018/3/4
# @Author : Zhujiagang
'''
@Description:使用随机游走算法求解函数极值
这里求解:f = sin(r)/r + 1,r = sqrt((x-50)^2+(y-50)^2)+e,0<=x,y<=100 的最大值
求解f的最大值，可以转化为求-f的最小值问题
'''
from __future__  import print_function
import math
import random
N = 100 # 迭代次数
step = 0.5 # 初始步长
epsilon = 0.00001
variables = 2 # 变量数目
x = [49,49] # 初始点坐标
walk_num = 1 # 初始化随机游走次数
print("迭代次数:",N)
print("初始步长:",step)
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
        u = [random.uniform(-1,1) for i in range(variables)] # 随机向量
        # u1 为标准化之后的随机向量
        u1 = [u[i]/math.sqrt(sum([u[i]**2 for i in range(variables)])) for i in range(variables)]
        x1 = [x[i] + step*u1[i] for i in range(variables)]
        if(function(x1) < function(x)): # 如果找到了更优点
            k = 1
            x = x1
        else:
            k += 1
    step = step/2
    print("第%d次随机游走完成。" % walk_num)
    walk_num += 1
print("随机游走次数:",walk_num-1)
print("最终最优点:",x)
print("最终最优值:",function(x))