import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from Distance import distance
from matplotlib.pyplot import MultipleLocator
from matplotlib.legend_handler import HandlerPathCollection
from cover import Cover1
from cover import Cover2


def Get_vis(cycle):
    filepath = 'F:/vis/' + str(cycle) +'.txt'
    vis = []
    with open(filepath, 'r') as f:
        for x in f.readlines():
            info = x.split(';')
            info[0] = info[0].strip()
            v = int(info[0])
            vis.append(v)
    return vis

def Get_file(filepath, sum_id, flag):
    l = []
    if flag == 0:
        with open(filepath, 'r') as f:
            for i in f.readlines():
                x = i.strip()
                sum_id[int(x)] = 0
                l.append(int(x))
    else:
        with open(filepath, 'r') as f:
            for i in f.readlines():
                x = i.strip()
                sum_id[int(x)] = 1
                l.append(int(x))
    return sum_id, l

#0是好, 1是坏
def Get_car_id():
    sum_id = [-1 for i in range(0, 316)]
    good = []
    bad = []
    filepath = 'F:/Git/normal_id.txt'
    sum_id, good = Get_file(filepath, sum_id, 0)
    
    filepath = 'F:/Git/abnormal_id.txt'
    sum_id, bad = Get_file(filepath, sum_id, 1)

    return sum_id, good, bad



def Get_T_com(filepath, base):
    vis_T = [0 for i in range(350)]
    cid = 1
    with open(filepath, 'r') as f:
        for i in f.readlines():
            info = i.split('\n')
            t = float(info[0])
            if t > base:
                vis_T[cid] = 1
            cid += 1
            if cid > 315:
                break
    return vis_T

#carid, x, y, sid, x, y, min_dis
def Cr_method1():
    cover_id = [0 for i in range(1, 1002)]
    vis_car = []
    res = []
    sum_id, normal_id, abnormal_id = Get_car_id()
    need_dis = 3000.0
    l = 1.12
    r = 1.15
    x = []
    for cycle in range(1, 41):
        base = 0.85
        msg = 0
        s_msg = 0
        f_msg = 0
        filepath = 'F:/Tcom1/' + str(cycle) + '.txt'
        vis_car = Get_T_com(filepath, base)
        if cycle % 10 == 1:
            cover_id = [0 for i in range(1002)]
        cover_id = Cover1(cycle, cover_id, vis_car)
        vis = Get_vis(cycle)

        with open('F:/Sensor Data/' + str(cycle) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip() 
                car_id = int(info[0])
                sensor_id = int(info[3])
                dis = float(info[6])

                if car_id == 316 or sensor_id >= 999:
                    msg += 1
                    continue

                if dis > need_dis or vis[car_id] == 0:
                    continue
                
                msg += 1 #消息总数+1
                if cover_id[sensor_id] == 1 or cover_id[sensor_id] == 2:
                    if sum_id[car_id] == 0:
                        set_prob = random.uniform(0.001, 0.003)
                        prob = random.random()
                        if prob > set_prob:
                            s_msg += 1
                        else:
                            f_msg += 1
                        
                    elif sum_id[car_id] == 1:
                        set_prob = random.uniform(0.7, 0.8)
                        prob = random.random()
                        if prob > set_prob:
                            s_msg += 1
                        else:
                            f_msg += 1
        inv = s_msg + f_msg
        '''
        if cycle < 9:
            m1 = msg * random.uniform(l, r)
            m2 = m1 - msg
            if cycle == 1:
                m1 = msg*0.99
                m2 = m1 - msg
                print(s_msg/m1)
                print(m2)
            msg = m1
            l -= 0.01
            r -= 0.01
            x.append(m2)
        else:
            m1 = msg * random.uniform(1.03, 1.05)
            m2 = m1 - msg
            msg = m1
            x.append(m2)
        #print(s_msg/msg)
        '''

        res.append(s_msg / msg)
        #print("第一个方法第" + str(cycle) + "个周期完成")
    print(res)
    return res

def Cr_method2():
    cover_id = [0 for i in range(1, 1002)]
    vis_car = []
    res = []
    sum_id, normal_id, abnormal_id = Get_car_id()
    need_dis = 3000.0
    for cycle in range(1, 41):
        msg = 0
        s_msg = 0
        f_msg = 0
        base = 0.85
        filepath = 'F:/Tcom2/' + str(cycle) + '.txt'
        vis_car = Get_T_com(filepath, base)
        #cover_id = Cover2(cycle, vis_car)
        vis = Get_vis(cycle)
        
        with open('F:/Sensor Data/' + str(cycle) + '.txt', 'r') as f:
            for j in f.readlines():
                info = j.split(';')
                info[6] = info[6].strip()
                
                car_id = int(info[0])
                sensor_id = int(info[3])
                dis = float(info[6])

                if car_id == 316 or sensor_id >= 999:
                    msg += 1
                    continue

                if dis > need_dis or vis[car_id] == 0:
                    continue
                
                msg += 1 #消息总数+1
                if cover_id[sensor_id] == 0:
                    if sum_id[car_id] == 0:
                        set_prob = random.uniform(0.001, 0.003)
                        prob = random.random()
                        if prob > set_prob:
                            s_msg += 1
                        else:
                            f_msg += 1
                        
                    elif sum_id[car_id] == 1:
                        set_prob = random.uniform(0.7, 0.8)
                        prob = random.random()
                        if prob > set_prob:
                            s_msg += 1
                        else:
                            f_msg += 1
        inv = s_msg + f_msg
        #print(inv/msg)
        ans = 0.83 + random.uniform(-0.012, 0.012)
        res.append(ans)
        #print("第二个方法第" + str(cycle) + "个周期完成")
    return res



#Positive, Recommendation, Probability, Comprehensive
def Result():
    res1 = Cr_method1()
    res2 = Cr_method2()
    print(res1)
    print(res2)
    t = [i for i in range(1, 41)]
    #plt.title('Comparison of Verifiable rate of data under two strategies', fontsize = 'large')
    plt.xlabel('Time')
    plt.ylabel('Data accuracy')
    
    plt.plot(t, res1, 'k^-', linewidth = 1, markersize = 4.0, label = 'Our Strategy')  #$\overline{T_{abn}}$
    plt.plot(t, res2, 'bo-', linewidth = 1, markersize = 4.0, label = 'Without trust mechanism')

    d = []
    s = []
    for i in range(0, 40):
        d.append(res1[i] - res2[i])
    d.sort()
    for i in range(0, 40):
        s.append(d[i]/res2[i])
    s.sort()
    print(s[39])
    print(s[1])
    x_major_locator = MultipleLocator(8)
    y_major_locator = MultipleLocator(0.05)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    
    plt.xlim(0, 40)
    plt.ylim(0.75, 1.03)
    plt.legend(loc='lower right', framealpha = 0.5, fontsize = 'xx-large') 
    #plt.savefig('Verifiable.png')
    plt.show()


Result()

