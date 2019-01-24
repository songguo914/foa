#coding:utf-8
'''
author: liujingmin

I like it to be useful to you
'''
from random import random


def foa(maxgen, sizepop, obj_func, param_dim=2, param_thresh=[]):
    '''
    Fruit Fly Optimization Algorithm
    support set range for optimize parameter
    support N-dimension optimize
    
    Parameters
    ----------
    maxgen: 
        Iteration times
    sizepop: 
        Population size
    obj_func: 
        the min object function or the loss function
    param_dim: 
        the parameter dimension
    param_thresh: 
        the range of the waiting parameter
        example:param_thresh=[(-1, 10), (), (2, 5)]
    
    Returns
    -------
    best_smell_list:
        the best object (function) values of maxgen iterations
    best_param_list:
        the best parameters of maxgen iterations
    '''
    if 0 == len(param_thresh):
        param_thresh = [() for num in range(param_dim)]
    if len(param_thresh) != param_dim:
        raise ValueError("invalid call")
    
    #待优化参数不给上下限的，默认使用(-10, 10)
    for num in range(param_dim):
        if 0 == len(param_thresh[num]):
            param_thresh[num] = (-10, 10)
    
    #随机初始果蝇群里位置，获取振荡幅值
    params_vibration = []
    params_init = []
    for num in range(param_dim):
        low_thresh, high_thresh = param_thresh[num]
        params_vibration.append((high_thresh-low_thresh)*0.1)
        params_init.append(low_thresh + (high_thresh-low_thresh)*random())
    
    #记录每一次迭代所有果蝇的参数值和损失值
    params_list = list(range(sizepop))
    smell_list  = list(range(sizepop))
    
    #记录所有迭代每次迭代的最佳值
    best_smell_list = list(range(maxgen))
    best_param_list = list(range(maxgen))

    # 果蝇寻优开始，利用嗅觉寻找食物
    for i in range(sizepop):
        #赋予果蝇个体利用嗅觉搜寻食物之随机方向与距离
        params_list[i] = [params_init[num]+params_vibration[num]*(2*random()-1) \
                for num in range(param_dim)]
        smell_list[i] = obj_func(*(params_list[i]))

    # 找出此果蝇群里中味道浓度最低的果蝇（求极小值）
    bestSmell = min(smell_list);
    bestindex = smell_list.index(bestSmell)

    #保留最佳味道浓度值与坐标，此时果蝇群利用视觉往该位置飞去
    params_init = params_list[bestindex]
    Smellbest = bestSmell;

    #果蝇迭代寻优开始
    for g in range(maxgen):
        #赋予果蝇个体利用嗅觉搜寻食物的随机方向和距离
        for i in range(sizepop):
            params_list[i] = [params_init[num]+params_vibration[num]*(2*random()-1) \
                    for num in range(param_dim)]
            smell_list[i] = obj_func(*(params_list[i]))

        #找出此果蝇群里中味道浓度最低的果蝇（求极小值）
        bestSmell = min(smell_list);
        bestindex = smell_list.index(bestSmell)

        #判断味道浓度是否优于前一次迭代味道浓度，若是则保留最佳味道浓度值与x，y的坐标，此时果蝇群体利用视觉往该位置飞去
        if bestSmell < Smellbest:
            params_init = params_list[bestindex]
            Smellbest = bestSmell

        #每次最优Semll值记录到yy数组中，并记录最优迭代坐标
        best_smell_list[g]    = Smellbest;
        best_param_list[g] = params_init;
    return best_smell_list, best_param_list


if "__main__" == __name__:
    def test_obj_func1(x, y):
        return x**2 + y**2 - 3
    print(foa(20,20,test_obj_func1)[0][-1])
    
    def test_obj_func2(x, y, z):
        return x**2 + y**2 + z**2 + 4
    print(foa(20,20,test_obj_func2, param_dim=3)[0][-1])
