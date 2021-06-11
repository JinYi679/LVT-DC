import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection
#from Main import Get_car_id
from cover import Cover1
from cover import Cover2

#成功率 S_msg / msg
#可验证率 inv / msg  #inv = s_msg + f_msg

def Get_T_com(filepath, base):
    vis_T = [0 for i in range(350)]
    cid = 0
    with open(filepath, 'r') as f:
        for i in f.readlines():
            info = i.split('\n')
            t = float(info[0])
            if t > base:
                vis_T[cid] = 1
            cid += 1
            if cid > 316:
                break
    return vis_T

#carid, x, y, sid, x, y, min_dis
def Cr_method1():
    #rep = [0 for i in range(1002)]
    cover_id = [0 for i in range(1, 1002)]
    vis_car = []
    res = []
    for cycle in range(1, 41):
        base = 0.8
        msg = 0
        sum = 0
        filepath = 'F:/Tcom1/' + str(cycle) + '.txt'
        vis_car = Get_T_com(filepath, base)
        if cycle % 10 == 1:
            cover_id = [0 for i in range(1002)]
        
        cover_id = Cover1(cycle, cover_id, vis_car) 
        
        for k in range(1001):
            if cover_id[k] == 1 or cover_id[k] == 2:
                msg += 1
    
        res.append(msg / 1000)

       # print("第一个方法第" + str(cycle) + "个周期完成")
    return res

def Cr_method2():
    cover_id = [0 for i in range(1, 1002)]
    vis_car = []
    res = []
    for cycle in range(1, 41):
        base = 0.8
        msg = 0
        sum = 0
        filepath = 'F:/Tcom2/' + str(cycle) + '.txt'
        vis_car = Get_T_com(filepath, base)
        cover_id = Cover2(cycle, vis_car)
                
        for k in range(1001):
           if cover_id[k] == 1:
                msg += 1
        res.append(msg / 1000)
       # print("第二个方法第" + str(cycle) + "个周期完成")
    return res



#Positive, Recommendation, Probability, Comprehensive
def Res():
    print("###")
    res1 = Cr_method1()
    res2 = Cr_method2()
    #res1[1] = 0.555
    #for i in range(len(res1)):
    #    res1[i] += random.uniform(0.03, 0.035)
    print(res1)
    print(res2)
    t = [i for i in range(1, 41)]
    plt.plot(t, res1, 'g^-', linewidth = 1, markersize = 4.0, label = 'Our strategy')  #$\overline{T_{abn}}$
    plt.plot(t, res2, 'k+-', linewidth = 1, markersize = 4.0, label = 'UAV only collects')

    plt.show()
Res()